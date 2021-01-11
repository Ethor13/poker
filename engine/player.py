from card import Card
import json


class Player:

    PLAYER_NUMBER = 1
    ATTRS = ['name', 'cards', 'stack', 'chipsOnTable', 'committed']

    # either pass in a list of [name, stack] or a dict
    def __init__(self, **kwargs):
        self.name = f"Player {Player.PLAYER_NUMBER}"
        Player.PLAYER_NUMBER += 1
        self.cards = []
        # chips left in player's stack
        self.stack = 0
        # chips on the table in the current round of betting
        self.chipsOnTable = 0
        # chips put in on previous rounds of betting
        self.committed = 0
        
        for key, value in kwargs.items():
            if key in Player.ATTRS:
                if key == "cards":
                    val = list(
                        map(lambda x: Card.new(x['v'] + x['f'].lower()), value))
                    setattr(self, key, val)
                else:
                    setattr(self, key, value)

    def __str__(self):
        temp = vars(self).copy()
        cards_str_lst = map(lambda x: Card.int_to_str(x), self.cards)
        cards_dict_lst = list(
            map(lambda x: {'f': x[1].upper(), 'v': x[0]}, cards_str_lst))
        temp['cards'] = cards_dict_lst
        return json.dumps(temp, separators=(',', ':'))

    def __repr__(self):
        temp = vars(self).copy()
        cards_str_lst = map(lambda x: Card.int_to_str(x), self.cards)
        cards_dict_lst = list(
            map(lambda x: {'f': x[1].upper(), 'v': x[0]}, cards_str_lst))
        temp['cards'] = cards_dict_lst
        return json.dumps(temp, separators=(',', ':'))

    def formatted_dict(self):
        temp = vars(self).copy()
        cards_str_lst = map(lambda x: Card.int_to_str(x), self.cards)
        cards_dict_lst = list(
            map(lambda x: {'f': x[1].upper(), 'v': x[0]}, cards_str_lst))
        temp['cards'] = cards_dict_lst
        return temp

    def put_in_chips(self, chips):
        self.chipsOnTable += chips
        self.stack -= chips

    def next_round(self):
        self.committed += self.chipsOnTable
        self.chipsOnTable = 0
