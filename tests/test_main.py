import unittest
from uvnb import hello

class TestMain(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(hello(), "Hello from my_package!")

if __name__ == '__main__':
    unittest.main()