import unittest
from dithering_binning import DitheringBinning


class TestDitheringBinning(unittest.TestCase):
    """Testing Dithering Binning functions"""

    def setUp(self):
        self.db_object = DitheringBinning()
        self.x = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.weights = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.labels = ['b1', 'b2', 'b3']
        self.label_length = len(self.labels)

    def test_setup_coins(self):
        """Should set and empty(dataless) DB object. It shouldn't allow uneven weights and values"""
        self.db_object.setup_coins([], [])  # empty test
        self.assertEqual(0, self.db_object.total_weight)
        self.assertEqual(0, len(self.db_object.coin_list))

        self.assertRaises(ValueError, self.db_object.setup_coins, [1, 2], [0])  # test uneven weights and values

        self.db_object.setup_coins(self.x, self.weights)
        self.assertEqual(9, self.db_object.total_weight)
        for i in range(0, 9):
            self.assertEqual(i, self.db_object.coin_list[i].value)

    def test_setup_bins(self):
        """Shuoldn't allow empty bins and should normally create labels"""
        self.assertRaises(ValueError, self.db_object.setup_bins, [], 0, 0)  # empty test

        self.db_object.setup_bins(self.labels, self.label_length, len(self.x))
        self.assertEqual(3, len(self.db_object.bins))  # Check lengths
        self.assertEqual(9, len(self.db_object.label))

        self.assertEqual('b1', self.db_object.bins[0].label)  # Check Bin Label
        self.assertEqual('b2', self.db_object.bins[1].label)
        self.assertEqual('b3', self.db_object.bins[2].label)

    def test_distribution_by_value(self):
        """Each Number should be distributed evenly by range value of each bin"""
        self.db_object.setup_coins(self.x, self.weights)
        self.db_object.setup_bins(self.labels, self.label_length, len(self.x))
        self.db_object.distribution_by_value()

        for bin_index, bucket in enumerate(self.db_object.bins):  # 0-2, 3-5, 6-8
            for coin_index, coin in enumerate(bucket.coins.values()):
                self.assertEqual(coin_index + (self.label_length * bin_index), coin.value)

    def test_reverse_distribution_by_value(self):
        """Distribution by values with reverse number"""
        self.x.reverse()
        self.db_object.setup_coins(self.x, self.weights)
        self.db_object.setup_bins(self.labels, self.label_length, len(self.x))
        self.db_object.distribution_by_value()

        against = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

        for bin_index, bucket in enumerate(self.db_object.bins):
            for coin_index, coin in enumerate(bucket.coins.values()):
                self.assertIn(coin.value, against[bin_index])

    def test_negative_distribution_by_value(self):
        """Negative values should be able to pass"""
        self.x.append(-10)
        self.weights.append(1)
        self.db_object.setup_coins(self.x, self.weights)
        self.db_object.setup_bins(self.labels, self.label_length, len(self.x))
        self.db_object.distribution_by_value()

    def test_dithering_balanced_values(self):
        """Values should be in-order in a balanced binning"""
        self.db_object.binning(self.x, self.weights, self.labels, self.label_length)
        for bin_index, bucket in enumerate(self.db_object.bins):
            for coin_index, coin in enumerate(bucket.coins.values()):
                self.assertEqual(coin_index + (self.label_length * bin_index), coin.value)

    def test_labeling(self):
        """Labels of bins should come out in order with None and NaN added in the end"""
        self.x.append(float('nan'))  # Handling None and Nan Values
        self.x.append(None)
        self.weights.append(1)
        self.weights.append(1)
        self.db_object.binning(self.x, self.weights, self.labels, self.label_length)

        against = ['b1', 'b1', 'b1', 'b1', 'b1', 'b2', 'b2', 'b3', 'b3', 'NaN', 'NaN']

        for i, label in enumerate(self.db_object.label):
            self.assertEqual(against[i], self.db_object.label[i])

    def test_db_value_inbalance(self):
        """"Creating a bunch of 9's and 10's to overflow 2nd and 3rd bin."""
        self.x.append(1)
        for i in range(0, 45):
            self.x.append(9)
        for i in range(0, 45):
            self.x.append(10)
        self.weights = [1] * len(self.x)
        self.db_object.binning(self.x, self.weights, self.labels, self.label_length)

        for coin in self.db_object.bins[0].coins.values():
            self.assertNotEqual(10, coin.value)  # No values should be 10
        for coin in self.db_object.bins[1].coins.values():
            self.assertFalse(coin.value < 9)  # Values should only be 9 or 10
        for coin in self.db_object.bins[2].coins.values():
            self.assertEqual(10, coin.value)  # Values can only be 10

    def test_db_weight_inbalance(self):
        """Created a weight in balance with a lot of weight on end but should evenly distribute)"""
        for i in range(0, 3):
            self.x.append(i + 8)
            self.weights.append(3)
        self.db_object.binning(self.x, self.weights, self.labels, self.label_length)

        for i in range(0, self.label_length):
            self.assertEqual(6, self.db_object.bins[i].weight)

    def test_db_zero_weights(self):
        """"Weights with 0's should be = to distribution to value"""
        x = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
        weights = [0] * len(x)
        self.db_object.binning(x, weights, self.labels, self.label_length)
        for i in range(0, self.label_length):
            self.assertEqual(5, len(self.db_object.bins[i]))

    def test_db_floats(self):
        """"Floats should also be able to work normally in dithering balance"""
        x = [1.1, 1.1, 1.1, 1.1, 1.1, 2.2, 2.2, 2.2, 2.2, 2.2, 3.3, 3.3, 3.3, 3.3, 3.3]
        weights = [0] * len(x)
        self.db_object.binning(x, weights, self.labels, self.label_length)

        against = [1.1, 2.2, 3.3]
        for i, bucket in enumerate(self.db_object.bins):
            for coin in bucket.coins.values():
                self.assertEqual(against[i], coin.value)


if __name__ == '__main__':
    unittest.main()