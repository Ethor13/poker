from deck import Deck
from player import Player
import json


class Table:

    # max_players must be greater than 1
    def __init__(self, sb, bb, max_players=8):
        self.max_players = max_players
        self.players = [None] * self.max_players
        self.deck = Deck()
        self.dealer = -1
        self.sb = -1
        self.bb = -1
        self.blinds = (sb, bb)
        self.board = []
        self.pot = 0
        self.action_order = []

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

    def take_player_cards(self):
        for p in self.players:
            if p is not None:
                p.cards = []

    def get_player_json(self):
        player_list = [None] * self.max_players
        for i, p in enumerate(self.players):
            if p is not None:
                p_dict = {name: p.name, stack: p.stack,  onTable: p.chipsOnTable,
                          hasCards: i in self.action_order, cards: p.cards}
                player_list[i] = p_dict
        return json.dumps(player_list)

    def set_preflop_action_order(self):
        '''
            Assumes that buttons haven't been moved yet from previous round
        '''
        order = []
        for i in range(1, self.max_players + 1):
            seat = (self.bb + i) % self.max_players
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
        self.action_order = self.action_order[i+1:] + self.action_order[:i+1]

    def active_players(self):
        count = 0
        for seat in self.action_order:
            if self.players[seat].stack > 0:
                count += 1
        return count

    def __str__(self):
        return str(self.players)

    def __repr__(self):
        return str(self.players)
