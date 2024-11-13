import unittest
from application.app import app

class CryptoPriceServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to the Crypto Price Service", response.data)

    def test_bitcoin_price(self):
        response = self.client.get('/bitcoin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'bitcoin', response.data)

    def test_ethereum_price(self):
        response = self.client.get('/ethereum')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ethereum', response.data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()