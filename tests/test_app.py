import unittest
from src.app import app

class AppTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_version(self):
        response = self.app.get('/version')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['version'], 'v0.0.1')

    def test_temperature(self):
        response = self.app.get('/temperature')
        self.assertEqual(response.status_code, 200)
        self.assertIn('average_temperature', response.json)

if __name__ == '__main__':
    unittest.main()
