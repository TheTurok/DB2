import math

class Bucket:
    """Bins to hold coin values.

    Attributes:
        _label (str): Buckets's label
        _weight (int): Buckets's weight, coin's total weight
        _coins (object: coin): The coins inside this bucket with index as its key
    """

    def __init__(self, label):
        #commenting STUFF GIT PULL SHIT LMAOasdasaSDASDas
        self._label = label
        self._weight = 0
        self._coins = {}

    def __str__(self):
        values = [coin.value for coin in self.coins.values()]
        return f"Bin: {self.label} -- Weight {self.weight} -- Coins: {values}"

    def __len__(self):
        return len(self.coins)

    @property
    def label(self):
        """str: Property of buckets's label"""
        return self._label

    @property
    def coins(self):
        """:dict:'coin': Property of bucket's coins"""
        return self._coins

    @property
    def weight(self):
        """int: Property of the bucket's weight, total amount of coin's weights"""
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    def add_coin(self, coin, index):
        """Add coin into bucket with its index from list as key

        Args:
            coin: the coin object to put into the coins dict
            index: the key the coin will have
        """
        if index in self.coins:
            raise ValueError('Coin with unique index already exists')
        if index < 0:
            raise ValueError('Invalid Index: Coin index cannot be below zero')
        if isinstance(coin.value, (int, float)) and not math.isnan(coin.value):
            self.weight += coin.weight
            self.coins[index] = coin

    def remove_coin(self, index):
        """Remove coin from the bucket with its index from list as key

        Args:
            index: the key of coin to remove

        Returns:
             Returns the index and coin removed
        """
        if index < 0:
            raise ValueError('Invalid Index: Coin index cannot be below zero')
        if index in self.coins:
            coin = self.coins[index]
            self.weight -= coin.weight
            del self.coins[index]
            return coin
        else:
            raise ValueError('Index is not in this bin')


