from typing import List, Dict, Union
from sqlalchemy import Engine


class DBService:
    """
    Class that handles database services such as fetching data from the database
    """

    engine: "Engine"

    def __init__(self) -> None:
        """
        Read database configuration from config.ini and create engine

        Information is pulled from the config file as a form of
        obfuscation to protect sensitive information.
        """
    ...

    def fetch_data(self, query: str) -> Union[str, List[Dict[str, Union[str, int, float]]]]:
        """
        Execute query and return result

        :param query: A string representing the query to be executed
        :return: If successful, a zipped list of dictionaries representing the result of the query, else False
        """
        ...

    @staticmethod
    def _is_safe_query(query: str) -> bool:
        """
        Private method that checks if query is safe by utilising regex to
        search for any unsafe keywords

        :param query: A string representing the query to be checked
        :return: True if query is safe, else False
        """
        ...

    @staticmethod
    def _get_zip_fields(query: str) -> Union[str, List[str]]:
        """
        Private method that returns a list of fields from the query string.
        If * is used, returns all fields.
        Lowercases the query string to ensure consistency.

        :param query: A string representing the query to be checked
        :return: A list of strings representing the fields from the query
        """
        ...
