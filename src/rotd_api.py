from flask import Flask, request, jsonify
from services import db_service
from log import ROTDlog
import configparser
import os

# Set up configuration, logging, and database service
config_file = os.path.join(os.path.dirname(__file__), "./config.ini")
log_location = os.path.join(os.path.dirname(__file__), "./log/ROTDlog.log")
logger = ROTDlog.ROTDLogging(log_location).get_logger()
config = configparser.ConfigParser()
config.read(config_file)
db = db_service.DBService()

# Set up Flask app, log start
app = Flask(__name__)
logger.info("\n\n-----------ROTD API started-----------")


@app.before_request
def check_api_key():
    # Get IP address of sender, check API key, return error if not authorized
    sender_ip = request.remote_addr
    api_key = request.headers.get("Authorization")
    if api_key != config['API']['API_KEY']:
        logger.error(f"{sender_ip} ::401:: Unauthorized access")
        return jsonify({"error": "Unauthorized"}), 401


@app.route("/fetch_data", methods=["POST"])
def fetch_data():
    # Get IP address of sender
    sender_ip = request.remote_addr
    try:
        # Get query parameter from request, log request
        data = request.json
        query = data.get("query")
        logger.info(f"Received from {sender_ip}: {data}")

        # Check if query parameter is provided, return error if not, log error
        if not query:
            logger.error(f"{sender_ip} ::400:: Query parameter not provided")
            return jsonify({"error": "Query parameter is required"}), 400

        # Execute query
        result = db.fetch_data(query)

        # If query is potentially unsafe, log error, return error message
        if result == "unsafe":
            logger.error(f"{sender_ip} ::403:: Unauthorised query: {query}")
            return jsonify({"error": "Please only use SELECT when executing a query"}), 403

        # If selected table doesn't exist, log error, return error message
        if result == "Table error":
            logger.error(f"{sender_ip} ::400:: Table does not exist")
            return jsonify({"error": "Selected table does not exist"}), 400

        # If unhandled error, log error, return error result
        if ":Other:" in result:
            result = result.strip(":Other:")
            logger.error(f"{sender_ip} ::500:: Other error: {result}")
            return jsonify({"error": f": {result}"}), 500

        # Query successful, log success, return result
        logger.info(f"{sender_ip} ::200:: Query successful")
        return jsonify(result), 200

    except Exception as e:
        # Log general function failure, return exception message
        logger.error(f"{sender_ip} :: Error:: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
