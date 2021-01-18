from deck import Deck
from player import Player
import json
from card import Card


class Table:

    ATTRS = ['max_players', 'players', 'deck', 'dealer', 'sb', 'bb', 'blinds',
             'board', 'pot', 'onTable', 'action_order', 'action_index', 'turn',
             'valid_moves', 'valid_raise_amts', 'to_go', 'stage', 'last_decision']

    # max_players must be greater than 1
    def __init__(self, **kwargs):
        self.max_players = 8
        self.players = [None] * self.max_players
        self.deck = Deck()
        self.dealer = -1
        self.sb = -1
        self.bb = -1
        self.blinds = [0, 0]
        self.board = []
        self.pot = 0
        self.onTable = 0
        self.action_order = []
        self.action_index = -1
        self.turn = -1
        self.valid_moves = []
        self.valid_raise_amts = [0, 0]
        self.to_go = 0
        # self.stage = 0='Start' | 1='Pre-flop' | 2='Post-flop' | 3='Post-turn' | 4='Post-river' | 5='Showdown'
        self.stage = 0
        # self.last_decision = 'Start' | 'Fold' | 'Check' | 'Call' | 'Raise ###'
        self.last_decision = 'Start'
        for key, value in kwargs.items():
            if key in Table.ATTRS:
                if key == "board":
                    val = list(
                        map(lambda x: Card.new(x['v'] + x['f'].lower()), value))
                    setattr(self, key, val)
                elif key == "players":
                    val = list(map(lambda x: Player(**x)
                                   if x is not None else None, value))
                    setattr(self, key, val)
                elif key == "deck":
                    val = Deck(value)
                    setattr(self, key, val)
                else:
                    setattr(self, key, value)

    def add_player(self, player, seat=None):
        if player in self.players:
            raise Exception("Player is already at table")
        if seat != None:
            if self.players[seat] == None:
                self.players[seat] = player
            else:
                raise Exception("Seat is taken")
        else:
            try:
                seat = self.players.index(None)
                self.players[seat] = player
            except ValueError:
                raise Exception("No Seats Available")

    def remove_player(self, player):
        try:
            seat = self.players.index(player)
            self.players[seat] = None
        except ValueError:
            raise Exception("Player not found")

    def take_player_cards(self, p):
        if p is not None:
            p.cards = []

    def take_players_cards(self):
        for p in self.players:
            if p is not None:
                p.cards = []

    def set_preflop_action_order(self):
        '''
            Assumes that buttons haven't been moved yet from previous round
        '''
        # find seat of player first to act last round
        first = None
        for i in range(1, self.max_players + 1):
            seat = (self.bb + i) % self.max_players
            p = self.players[seat]
            if p is not None and p.stack > 0:
                first = seat
                break
        assert first != None, "Invalid Preflop Ordering"

        order = []
        for i in range(1, self.max_players + 1):
            seat = (first + i) % self.max_players
            p = self.players[seat]
            if p is not None and p.stack > 0:
                order.append(seat)
        self.action_order = order

    def set_postflop_action_order(self):
        '''
            Uses the last round's action_order to create the next round's action_order
        '''
        order = []
        for i in range(1, self.max_players + 1):
            seat = (self.dealer + i) % self.max_players
            if seat in self.action_order:
                order.append(seat)
        self.action_order = order


    def adjust_action_order(self, seat):
        '''
            called when player at seat raises and becomes the last to act
        '''
        # index of seat in action_order
        i = self.action_order.index(seat)
        self.action_order = self.action_order[i:] + self.action_order[:i]

    def active_players(self):
        count = 0
        for seat in self.action_order:
            if self.players[seat].stack > 0:
                count += 1
        return count

    def __str__(self):
        temp = vars(self).copy()
        # p = list(map(lambda x: str(x) if x is not None else x, self.players))
        p = list(map(lambda x: x.formatted_dict()
                     if x is not None else None, self.players))
        d = self.deck.cards
        b_temp = map(lambda x: Card.int_to_str(x), self.board)
        b = list(
            map(lambda x: {'f': x[1].upper(), 'v': x[0]}, b_temp))
        temp['players'] = p
        temp['deck'] = d
        temp['board'] = b
        return json.dumps(temp, separators=(',', ':'))

    def __repr__(self):
        temp = vars(self).copy()
        # p = list(map(lambda x: str(x) if x is not None else x, self.players))
        p = list(map(lambda x: x.formatted_dict()
                     if x is not None else None, self.players))
        d = self.deck.cards
        b_temp = map(lambda x: Card.int_to_str(x), self.board)
        b = list(
            map(lambda x: {'f': x[1].upper(), 'v': x[0]}, b_temp))
        temp['players'] = p
        temp['deck'] = d
        temp['board'] = b
        return json.dumps(temp, separators=(',', ':'))
