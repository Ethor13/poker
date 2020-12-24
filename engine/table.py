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
        self.turn = -1
        self.blinds = (sb, bb)
        self.board = [None] * 5
        self.pot = 0

    def add_player(self, player, seat=None):
        if player in self.get_players():
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

    def get_players(self):
        return self.players

    def get_player(self, i):
        return self.players[i]

    def get_player_chips(self, i):
        return self.players[i].get_chips()

    # number of players with chips at the table
    def get_num_players(self):
        count = 0
        for p in self.players:
            if p != None and p.get_chips() > 0:
                count += 1
        return count

    def get_dealer(self):
        return self.dealer

    def set_dealer(self, i):
        self.dealer = i

    def get_blinds(self):
        return self.blinds

    def set_blinds(self, sb, bb):
        self.blinds = (sb, bb)

    def get_sb(self):
        return self.sb

    def set_sb(self, s):
        self.sb = s

    def get_bb(self):
        return self.bb

    def set_bb(self, b):
        self.bb = b

    def get_board(self):
        return self.board

    def reset_board(self):
        self.board = [None] * 5

    def set_board_card(self, i, card):
        self.board[i] = card

    def get_pot(self):
        return self.pot

    def set_pot(self, pot):
        self.pot = pot

    def add_to_pot(self, amt):
        self.pot += amt

    def get_player_seat(self, player):
        try:
            return self.players.index(player)
        except:
            raise Exception("Player not found")

    def take_player_cards(self):
        for p in self.get_players():
            if p is not None:
                p.set_cards([])

    def get_player_json(self):
        player_list = []
        for player in self.get_players():
            p_dict = {name: player.get_name(), stack: player.get_chips(), onTable: player.get_chips_on_table(
            ), hasCards: player.is_playing(), cards: player.get_cards()}
            player_list.append(p_dict)
        return player_list

    def get_player_turn(self):
        return self.turn

    def set_player_turn(self, i):
        self.turn = i

    def inc_player_turn(self):
        self.turn = (self.turn + 1) % self.max_players

    def __str__(self):
        return str(self.players)

    def __repr__(self):
        return str(self.players)
