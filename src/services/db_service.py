from sqlalchemy import create_engine, text
import configparser
import re
import os

config_file = os.path.join(os.path.dirname(__file__), "../config.ini")

# Get all fields from the traffic_data table from relative directory
if __name__ == "__main__":
    from data_struct import all_fields
else:
    from .data_struct import all_fields


class DBService:
    def __init__(self):
        # Read database configuration from config.ini and create engine
        config = configparser.ConfigParser()
        config.read(config_file)
        database = config["database"]["DB_NAME"]
        user = config["database"]["DB_USER"]
        password = config["database"]["DB_PASSWORD"]
        host = config["database"]["DB_HOST"]
        port = config["database"]["DB_PORT"]
        self.engine = create_engine(f"postgresql+pg8000://{user}:{password}@{host}:{port}/{database}")

    def fetch_data(self, query):
        # Check if query is safe, return messsage if not
        try:
            if not self._is_safe_query(query):
                return "unsafe"
            else:
                # Execute query and return result
                fields = self._get_zip_fields(query)
                with self.engine.connect() as connection:
                    result = connection.execute(text(query))
                    table_data = [dict(zip(fields, row)) for row in result]
                return table_data
        except Exception as e:
            # Return error message if table doesn't exist
            if 'relation' in str(e):
                return "Table error"

            # Return error message for any other error
            else:
                return ":Other:" + str(e)

    @staticmethod
    # Check if query is safe by checking for any unsafe keywords
    def _is_safe_query(query):
        return not re.search(r'\b(INSERT|UPDATE|DELETE|DROP|ALTER|TRUNCATE)\b', query, re.IGNORECASE)

    @staticmethod
    # Get fields from query, return all fields if * is used
    def _get_zip_fields(query):
        fields = query.split("SELECT")[1].split("FROM")[0].strip()
        return all_fields if fields == "*" else fields


if __name__ == "__main__":
    db = DBService()
    data = db.fetch_data("SELECT * FROM tabel LIMIT 10;")
    print(data)
    data = db.fetch_data("SELECT count_point_id, year, region_id FROM traffic_data LIMIT 10;")
    print(data)

