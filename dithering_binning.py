import time
import random

from coin import Coin
from bucket import Bucket


class DitheringBinning:
    """Class to distribute the coins in their appropriate bins according to its weight and values.

    Attributes:
        _coin_list (list: coin object): A list to hold values and weights after it has been converted to coins.
        _bins (list: bin object): A list of bins to distribute the coins into
        _min_value (int): The lowest value of a coin
        _max_value (int): The highest value of a coin
        _total_weight (int): total weight of all coins
        _bin_count (int): Number of bins\
        _label (str): Labels for respective values and weight
    """

    def __init__(self):
        self._coin_list = []
        self._bins = []
        self._min_value = None
        self._max_value = None
        self._total_weight = 0
        self._bin_count = 0
        self._label = []

    def __str__(self):
        db_info = ['Labeling:', self.label, '---', "Total Weight: " + str(self.total_weight), '---']
        for bucket in self.bins:
            db_info.append(bucket)
        return '\n'.join(map(str, db_info))

    @property
    def bins(self):
        """:obj:'list' of :obj:'bin': Property of DB bin list"""
        return self._bins

    @property
    def coin_list(self):
        """:obj:'list' of :obj:'coin': Property of DB coin list"""
        return self._coin_list

    @property
    def min_value(self):
        """int: Property of DB min value"""
        return self._min_value

    @min_value.setter
    def min_value(self, value):
        self._min_value = value

    @property
    def max_value(self):
        """int: Property of DB max value"""
        return self._max_value

    @max_value.setter
    def max_value(self, value):
        self._max_value = value

    @property
    def total_weight(self):
        """"int: Total weight of all the coin"""
        return self._total_weight

    @total_weight.setter
    def total_weight(self, value):
        self._total_weight = value

    @property
    def bin_count(self):
        """int: Property of DB number of bins"""
        return self._bin_count

    @bin_count.setter
    def bin_count(self, value):
        self._bin_count = value

    @property
    def label(self):
        """list: str: Holds all the respective value's binning"""
        return self._label

    def setup_coins(self, values, weights):
        """Turn the input of values and weight into coins

        set values for the min and max range for values

        Args:
            values: the input values
            weights: the weight of each value
        """
        if len(values) != len(weights):
            raise ValueError('Values and weight must have same number of inputs')

        for i in range(0, len(values)):  # Making Coins
            value = values[i]
            coin = Coin(value, weights[i])
            self.coin_list.append(coin)

            if isinstance(value, int):
                self.total_weight += weights[i]  # Sum total weight of coins
                if self.min_value is None or self.min_value > value:
                    self._min_value = value
                if self.max_value is None or self.max_value < value:
                    self.max_value = value

    def setup_bins(self, labels, count, length):
        """Setup empty label and empty bins with appropriate labels

        Args:
            labels: list of labels for the bins
            count: the number of bins
            length: Amount of binning values respective to input
        """
        if len(labels) == 0 or count == 0:
            raise ValueError('Must have at least one Bin!')

        for i in range(0, length):
            self.label.append('')  # Fill in Label Empty so we can insert values in its according index

        self.bin_count = count

        for i in range(0, count):
            empty_bin = Bucket(labels[i])
            self.bins.append(empty_bin)

    def _send_bin(self, offset_value, split):
        """Receive offset_value with split and calculate which bin it belongs too"""
        fit = 0
        while offset_value >= split:
            offset_value -= split
            fit += 1
        return fit

    def distribution_by_value(self):
        """Distribute coins into bins according to its value

        We use the range of min and max to create a split number by value per bin. The fit is made by calling _send_bin,
        which will keep reducing the fit number by split to find the appropriate bin it belongs into

        Since every index is unique, we will use that as key for coins to store it in bins.
        """

        split = int((1 + self.max_value - self.min_value) / self.bin_count)

        for index, coin in enumerate(self.coin_list):
            if not isinstance(coin.value, int):
                self.label[index] = 'NaN'
                continue

            offset_value = int(coin.value - self.min_value)
            fit = self._send_bin(offset_value, split)

            if fit >= self.bin_count:  # Edge Case: If fit hits the max value, put in last bin
                self.bins[self.bin_count - 1].add_coin(coin, index)
            else:
                self.bins[fit].add_coin(coin, index)

    def dithering_balance(self):
        """Balance the weight in each bin by moving coins around after coins are distributed in bins already.

        Using Dithering, we distribute min/max value of each bins and move around coins with random weight chosen until
        the weight in the bin are close to being evenly distributed. -- Start with in-order then reverse for
        full balance. Each run, we keep pushing to the next bin until its weight is less than the threshold.

        threshold
            1. Weight / number of bins: the least amount of weight in each bin
            2. Average weight in each coin: To not over add coins in a bin accounting with average value.
            3. Threshold >= : threshold is naturally bigger than a split even weight for each bin, so we use = sign to
            favor more balance/dithering, as it would be a ~5050 anyways for next value to make it go below split weight
        """

        split_weight = int(self.total_weight / self.bin_count)  # All bins weight is evenly split
        average_weight = int(self.total_weight / len(self.coin_list))  # Bins average weight per coin
        threshold = split_weight + average_weight  # Threshold to move coin to other bin

        # In-Order
        for i in range(0, self.bin_count-1):  # Loop until 2nd to last item
            bucket = self.bins[i]
            while bucket.weight >= threshold and bucket.weight != 0:  # Keep adding coins on next bin until it pass threshold
                max_value = max([v.value for v in bucket.coins.values()])  # Gat max value as going up the bin count
                filtered_values = {k: coin for (k, coin) in bucket.coins.items() if coin.value >= max_value}  # Edge Values
                coin_index = random.choice(list(filtered_values))  # Dithering Random weight of that value
                self.bins[i+1].add_coin(bucket.remove_coin(coin_index), coin_index)  # add removed coin

        for i in range(self.bin_count-1, 0, -1):  # Reverse
            bucket = self.bins[i]
            while bucket.weight >= threshold and bucket.weight != 0:
                min_value = min([v.value for v in bucket.coins.values()])  # Min values going down the bin count
                filtered_values = {k: coin for (k, coin) in bucket.coins.items() if coin.value <= min_value}
                coin_index = random.choice(list(filtered_values))
                self.bins[i-1].add_coin(bucket.remove_coin(coin_index), coin_index)

    def labeling(self):
        """Labeling the coins in the bins

        Returns:
            The label Output
        """

        for bucket in self.bins:
            for k, v in bucket.coins.items():
                self.label[k] = bucket.label  # coin key respective to value index

        return self.label

    def binning(self, x, weight, bin_label, bin_count):
        """Calling all the functions to perform Dithering for the coin distributions

        This function was mainly made to run the program all at once. We can call the inner functions piece by piece for
        more control and testing purposes.

        Args:
            x: values
            weight: weight of the values
            bin_label: list bin labels
            bin_count: the number of bins

        Returns:
            The label Output
        """

        if len(bin_label) != bin_count:
            raise ValueError('length of labels much match bin_count')

        self.setup_bins(bin_label, bin_count, len(x))  # Setup Coins and Empty Bins
        self.setup_coins(x, weight)
        self.distribution_by_value()  # Distribute by value initially
        self.dithering_balance()  # Balance weights afterwards

        return self.labeling()


if __name__ == "__main__":
    start_time = time.time()

    # Change Values Here to see Results!
    x = [-1, 0, 3, 4, 5, 6, 7, 8, float('nan'), 10, 1, 2, 3, 4, None, 6, 7, 8, 9, 10]
    weights = [1, 1, 1, 1, 5, 5, 1, 1, 4, 4, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    bin_labels = ['b1', 'b2', 'b3']
    number_of_bins = len(bin_labels)  # Probably don't want to touch this

    # Run Program and Print Values
    db = DitheringBinning()
    label = db.binning(x, weights, bin_labels, number_of_bins)

    print()
    print('Return of function')
    print(label)
    print()

    # Accuracy Testing
    for bucket in db.bins:
        split_weight = int(db.total_weight / db.bin_count)
        percent_off = (bucket.weight - split_weight) / db.total_weight
        print(str(bucket.label) + " is " + "{0:.2%}".format(abs(percent_off)) + " off from perfect distribution:")

    print()
    print('Dithering Binning Object')
    print(db)
    print()

    end_time = time.time()
    print("Total time to run this program: " + str(end_time-start_time) + " seconds")
