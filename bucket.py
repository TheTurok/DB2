

class Bucket:
    """Bins to hold coin values.

    Attributes:
        _label (str): Bin's label
        _weight (int): Bin's weight, coin's total weight
        _coins (object: coin): The coins inside this bin with index as its key
    """

    def __init__(self, label):
        self._label = label
        self._weight = 0
        self._coins = {}

    def __str__(self):
        list = [v.value for (k, v) in self.coins.items()]
        return "Bin: " + str(self.label) + " -- Weight: " + str(self.weight) + " -- Coins: " + str(list)

    def __len__(self):
        return len(self.coins)

    @property
    def label(self):
        """str: Property of bin's label"""
        return self._label

    @property
    def coins(self):
        """:dict:'coin': Property of bin's coins"""
        return self._coins

    @property
    def weight(self):
        """int: Property of the bin's weight, total amount of coin's weights"""
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    def add_coin(self, coin, index):
        """Add coin into bin with its index from list as key

        Args:
            coin: the coin object to put into the coins dict
            index: the key the coin will have
        """
        if index in self.coins:
            raise ValueError('Coin with unique index already exists')
        if index < 0:
            raise ValueError('Invalid Index: Coin index cannot be below zero')
        if isinstance(coin.value, int):
            self.weight += coin.weight
            self.coins[index] = coin

    def remove_coin(self, index):
        """Remove coin from the bin with its index from list as key

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


