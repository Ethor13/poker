class Player:

    def __init__(self, name, stack, ranges):
        self.name = name
        self.stack = stack
        self.ranges = ranges
        self.playing = False
        self.cards = []
        self.chipsOnTable = 0

    def get_name(self):
        return self.name

    def add_chips(self, amount):
        self.stack += amount

    def subtract_chips(self, amount):
        if self.stack - amount < 0:
            raise Exception("Can't have negative chips")
        self.stack -= amount

    def set_chips(self, amount):
        self.stack = amount

    def get_chips(self):
        return self.stack

    def get_cards(self):
        return self.cards

    def add_card(self, card):
        self.cards.append(card)

    def set_cards(self, cards):
        self.cards = cards

    def get_chips_on_table(self):
        return self.chipsOnTable

    def set_chips_on_table(self, chips):
        if chips > self.stack + self.chipsOnTable:
            raise Exception("Can't put more chips on table than player has")
        self.chipsOnTable = chips
        self.stack -= chips

    def add_chips_on_table(self, chips):
        if chips > self.chips:
            raise Exception("Can't put more chips on table than player has")
        self.chipsOnTable += chips
        self.stack -= chips

    def subtract_chips_on_table(self, chips):
        if self.chipsOnTable - chips < 0:
            raise Exception("Can't have negative chips on table")
        self.chipsOnTable -= chips
        self.stack += chips

    def is_playing(self):
        return self.playing

    def set_is_playing(self, b):
        self.playing = b

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
