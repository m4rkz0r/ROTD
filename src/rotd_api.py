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

        # Check if query is safe, return error if not, log error
        result = db.fetch_data(query)
        if not result:
            logger.error(f"{sender_ip} ::400:: Invalid query: {query}")
            return jsonify({"error": "Invalid query. Please only use SELECT"}), 400

        # Query successful, return result, log success
        logger.info(f"{sender_ip} ::200:: Query successful")
        return jsonify(result), 200

    except Exception as e:
        # Log error, return error message
        logger.error(f"{sender_ip} :: Error:: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
