import unittest
import os
from app import app  
class IntegrationTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        os.environ['SENSEBOX_TEMP'] = '20'  

    def test_metrics(self):
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'average_temperature', response.data)

    def test_temperature_good(self):
        os.environ['SENSEBOX_TEMP'] = '20'
        response = self.app.get('/temperature')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'Good')

    def test_temperature_too_cold(self):
        os.environ['SENSEBOX_TEMP'] = '5'
        response = self.app.get('/temperature')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'Too Cold')

    def test_temperature_too_hot(self):
        os.environ['SENSEBOX_TEMP'] = '40'
        response = self.app.get('/temperature')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertEqual(json_data['status'], 'Too Hot')

if __name__ == '__main__':
    unittest.main()
