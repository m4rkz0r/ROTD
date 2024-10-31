import unittest
from src.services.db_service import DBService
from src.services import data_struct


class TestDBService(unittest.TestCase):
    def setUp(self):
        self.service = DBService()

    def test_fetch_data_safe_query(self):
        # Test a safe query
        query = "SELECT road_category, road_name FROM traffic_data LIMIT 1;"
        result = self.service.fetch_data(query)
        expected_result = [{'r': 'MCU', 'o': 'U'}]
        self.assertEqual(result, expected_result)

    def test_is_safe_query(self):
        # Unsafe query
        self.assertFalse(self.service._is_safe_query("DROP TABLE traffic_data"))

        # Safe query
        self.assertTrue(self.service._is_safe_query("SELECT * FROM traffic_data"))

    def test_get_zip_fields(self):
        # Test a query with specific fields
        query = "SELECT road_category, road_name FROM traffic_data LIMIT 10;"
        result = self.service._get_zip_fields(query)
        self.assertEqual(result, "road_category, road_name")

        # Test query with all fields
        query_all = "SELECT * FROM traffic_data;"
        result_all = self.service._get_zip_fields(query_all)
        self.assertEqual(result_all, data_struct.all_fields)


if __name__ == "__main__":
    unittest.main()