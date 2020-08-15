class Player:
    def __init__(self, name):
        self.name = name
        self.rack = {}
        self.score = 0

    def add_letter(self, letter):
        if letter in self.rack:
            self.rack[letter] += 1
        else:
            self.rack[letter] = 1

    def remove_letter(self, letter):
        assert letter in self.rack
        assert self.rack[letter] > 0
        self.rack[letter] -= 1

    def fill_rack(self, bag):
        while sum(self.rack.values()) < 7:
            letter = bag.draw()
            if letter is None:
                break
            else:
                self.add_letter(letter)
