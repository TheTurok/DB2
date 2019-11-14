class Coin:
    """Coin Properties

    Attributes:
        _value (int): Value of the coin.
        _weight (int): the weight of the coin
    """

    def __init__(self, value, weight):
        self._value = value
        self._weight = weight

    @property
    def weight(self):
        """int: Property of coin's weight"""
        return self._weight

    @property
    def value(self):
        """int: Property of coin's value"""
        return self._value

