import random
from .DefaultSettings import DEFAULT_BAG_DIST

class Bag:
    def __init__(self):
        self.distribution = DEFAULT_BAG_DIST.copy()

    def draw(self, n=1):
        if sum(self.distribution.values()) == 0:
            return None
        letter = random.choices(list(self.distribution.keys()), weights=self.distribution.values())[0]
        self.distribution[letter] -= 1
        return letter
