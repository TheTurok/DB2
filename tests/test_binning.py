import unittest
from coin import Coin
from bucket import Bin


class TestBin(unittest.TestCase):
    """Testing Bin Class and functions"""

    def setUp(self):
        self.bin = Bin('test')
        c1 = Coin(1, 1)
        c2 = Coin(2, 2)
        c3 = Coin(3, 3)
        self.bin.add_coin(c1, 7)
        self.bin.add_coin(c2, 8)
        self.bin.add_coin(c3, 9)

    def test_bin_class(self):
        """Testing the class instance"""
        self.assertEqual('test', self.bin.label)
        self.assertEqual(6, self.bin.weight)
        self.assertEqual(3, len(self.bin))

    def test_add_coin(self):
        """Testing to add a coin and many different values"""
        c1 = Coin(-1, 1)
        self.bin.add_coin(c1, 0)  # Normal Coin with negative value
        self.assertEqual(4, len(self.bin))
        self.assertEqual(-1, self.bin.coins[0].value)
        self.assertEqual(1, self.bin.coins[0].weight)

        c2 = Coin(99, 2)
        self.bin.add_coin(c2, 3)
        self.assertEqual(5, len(self.bin))
        self.assertEqual(99, self.bin.coins[3].value)
        self.assertEqual(2, self.bin.coins[3].weight)
        self.assertEqual(9, self.bin.weight)  # Check total weight

        c3 = Coin(None, 3)
        self.bin.add_coin(c3, 2)  # None Value
        self.assertEqual(5, len(self.bin))

        c4 = Coin(float('nan'), 10)
        self.bin.add_coin(c4, 2)  # None Value
        self.assertEqual(5, len(self.bin))

        c6 = Coin(1, 1)
        self.assertRaises(ValueError, self.bin.add_coin, c6, 0)  # test adding coin in same index

        c5 = Coin(99, -1)
        self.assertRaises(ValueError, self.bin.add_coin, c5, 0)  # test adding coin with negative index
        self.assertEqual(5, len(self.bin))
        self.assertEqual(9, self.bin.weight)

    def test_remove_coin(self):
        """Testing remove_coin function"""
        self.assertRaises(ValueError, self.bin.remove_coin, -1)  # test removing negative index
        self.assertRaises(ValueError, self.bin.remove_coin, 99)  # not in bin
        c1 = self.bin.remove_coin(9)
        self.assertEqual(3, c1.weight)
        self.assertEqual(3, c1.value)
        self.assertEqual(3, self.bin.weight)
        self.assertEqual(2, len(self.bin))


if __name__ == '__main__':
    unittest.main()

