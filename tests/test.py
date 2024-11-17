import unittest
from app import bp

class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = bp.test_client()
        
    def test_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Hello, Docker!')

if __name__ == '__main__':
    unittest.main()