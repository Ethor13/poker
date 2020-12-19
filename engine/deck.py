import itertools
import random


class Deck:

    # Ace is 14
    values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    suits = [1, 2, 3, 4]
    cards = list(itertools.product(values, suits))

    def __init__(self):
        self.cards = random.sample(Deck.cards, len(Deck.cards))
        self.index = len(Deck.cards)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.cards[self.index]

    def deal_card(self):
        return next(self)

    def deal_cards(self, i):
        s = set()
        for _ in range(i):
            s.add(next(self))
        return s

    def shuffle(self):
        self = Deck()
