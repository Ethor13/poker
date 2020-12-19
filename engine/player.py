class Player:

    def __init__(self, name, chips, ranges):
        self.name = name
        self.chips = chips
        self.ranges = ranges
        self.cards = []

    def get_name(self):
        return self.name

    def add_chips(self, amount):
        self.chips += amount

    def subtract_chips(self, amount):
        if self.chips - amount < 0:
            raise Exception("Can't have negative chips")
        self.chips -= amount

    def set_chips(self, amount):
        self.chips = amount

    def get_chips(self):
        return self.chips

    def get_cards(self):
        return self.cards

    def add_card(self, card):
        self.cards.append(card)

    def set_cards(self, cards):
        self.cards = cards

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
