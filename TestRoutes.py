import unittest

from app.routes import login


class TestRoutes(unittest.TestCase):
    def test_login(self):
        test1 = {
            'username': 'Man',
            'email': 'GoodBoy',
            'password': 'qwerty'
        }
        test2 = {
            'username': 'F',
            'email': 'FF',
            'password': 'FFF'
        }
        response1 = {
            'response': 'ok',
            'username': test1['username'],
            'surname': 'GoodBoy',
            'email': test1['email'],
        }
        response2 = {
            'error': 'Not found'
        }
        self.assertEqual(login(test1), response1)
        self.assertEqual(login(test2), response2)

    def test_registration(self):
        pass
