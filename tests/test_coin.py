import unittest
from coin import Coin


class TestCoin(unittest.TestCase):
    """Testing Coin Class"""

    def test_coin(self):
        """Testing Coin object instance"""
        c = Coin(1, 9)
        self.assertEqual(1, c.value)
        self.assertEqual(9, c.weight)


if __name__ == '__main__':
    unittest.main()
