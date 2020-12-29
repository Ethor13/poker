class Player:

    def __init__(self, name, stack, ranges):
        self.name = name
        self.ranges = ranges
        self.cards = []
        # chips left in player's stack
        self.stack = stack
        # chips on the table in the current round of betting
        self.chipsOnTable = 0
        # chips put in on previous rounds of betting
        self.committed = 0

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def put_in_chips(self, chips):
        self.chipsOnTable += chips
        self.stack -= chips

    def next_round(self):
        self.committed += self.chipsOnTable
        self.chipsOnTable = 0
