import unittest
import requests


class APISecurityTestCase(unittest.TestCase):
    def setUp(self):
        # Sets up the test client for our Flask app
        self.base_url = "http://127.0.0.1:5000/fetch_data"
        self.api_key = "690a1bbf-8acf-4f37-bef1-d34cca2db8f1"

    def test_fetch_data(self):
        # Define a valid fetch request data and headers
        request_data = {
            "query": "SELECT * FROM traffic_data LIMIT 10;"
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key
        }

        # Make a POST request to the /fetch_data endpoint
        response = requests.post(
            self.base_url,
            json=request_data,
            headers=headers
        )

        # Parse the response data
        data = response.json()

        # Perform assertions to verify the response
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_sql_injection_drop_table(self):
        # Test with a malicious query attempting to drop a table
        request_data = {
            "query": "DROP TABLE traffic_data;"
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

        # Make the POST request
        response = requests.post(
            self.base_url,
            json=request_data,
            headers=headers
        )

        # Expect the request to fail with a 400 Bad Request or similar
        self.assertNotEqual(response.status_code, 200)

    def test_sql_injection_delete_data(self):
        # Test with a malicious query attempting to delete data
        request_data = {
            "query": "DELETE FROM traffic_data;"
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

        # Make a POST request to the /fetch_data endpoint
        response = requests.post(
            self.base_url,
            json=request_data,
            headers=headers
        )

        # Expect the request to fail with a 400 Bad Request or similar
        self.assertNotEqual(response.status_code, 200)

    def test_sql_injection_update_data(self):
        # Test with a malicious query attempting to modify data
        request_data = {
            "query": "UPDATE traffic_data SET easting = '1018008135';"
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

        # Make a POST request to the /fetch_data endpoint
        response = requests.post(
            self.base_url,
            json=request_data,
            headers=headers
        )

        # Expect the request to fail with a 400 Bad Request or similar
        self.assertNotEqual(response.status_code, 200)

    def test_only_select_queries_allowed(self):
        # Test that a non-SELECT query returns an error
        request_data = {
            "query": "INSERT INTO traffic_data (easting) VALUES ('1018008135');"
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

        # Make a POST request to the /fetch_data endpoint
        response = requests.post(
            self.base_url,
            json=request_data,
            headers=headers
        )

        # Assert that the response status code indicates rejection of non-SELECT queries
        self.assertNotEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
