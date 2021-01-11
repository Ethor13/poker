from table import Table
from evaluator import Evaluator
from card import Card
import signal
import sys

signal.signal(signal.SIGINT, signal.SIG_DFL)


class Game:

    def __init__(self, table):
        self.table = table

    def has_min_players(self):
        '''
            Assumes that set_preflop_action_order has already been called
        '''
        if len(self.table.action_order) < 2:
            raise Exception("Not enough players")

    def move_buttons(self):
        '''
            Assumes that has_min_players has already been called
        '''
        self.table.bb = self.table.action_order[-1]
        self.table.sb = self.table.action_order[-2]

        if len(self.table.action_order) == 2:
            self.table.dealer = self.table.action_order[-1]
        else:
            self.table.dealer = self.table.action_order[-3]

    def deal(self):
        for seat in self.table.action_order:
            self.table.players[seat].cards = self.table.deck.draw(2)

    def deal_flop(self):
        self.table.board = self.table.deck.draw(3)

    def deal_turn(self):
        self.table.board.append(self.table.deck.draw())

    def deal_river(self):
        self.table.board.append(self.table.deck.draw())

    def preflop(self):
        '''
            Assumes set_preflop_action_order has already been called
        '''
        p_sb = self.table.players[self.table.sb]
        p_bb = self.table.players[self.table.bb]
        sb_amt_adj = min(self.table.blinds[0], p_sb.stack)
        bb_amt_adj = min(self.table.blinds[1], p_bb.stack)
        p_sb.put_in_chips(sb_amt_adj)
        p_bb.put_in_chips(bb_amt_adj)
        self.table.onTable += sb_amt_adj + bb_amt_adj

        self.table.to_go = self.table.blinds[1]
        self.table.valid_raise_amts[0] = 2 * self.table.blinds[1]

    def post_flop(self):
        '''
            Assumes set_postflop_action_order has already been called
        '''
        self.table.to_go = 0
        self.table.valid_raise_amts[0] = self.table.blinds[1]

    def valid_moves(self, player, active_players):
        moves = None
        if self.table.to_go > player.chipsOnTable:
            moves = ['Fold', 'Call']
            if active_players > 1 and player.stack > self.table.to_go:
                moves.append('Raise')
        else:
            moves = ['Check', 'Raise']
        return moves

    def round_of_action(self):
        flag = False

        if self.table.last_decision == "Start":
            self.table.action_index = 0

            # skip while loop if only one person can make a move
            if self.table.active_players() < 2:
                self.table.action_index = len(self.table.action_order)

        while self.table.action_index < len(self.table.action_order) and len(self.table.action_order) > 1:
            action_seat = self.table.action_order[self.table.action_index]
            action_player = self.table.players[action_seat]
            if action_player.stack > 0:
                if self.table.last_decision == "Start" or flag:
                    self.table.turn = action_seat
                    self.table.valid_moves = self.valid_moves(
                        action_player, self.table.active_players())
                    self.table.valid_raise_amts[1] = action_player.stack + \
                                                    action_player.chipsOnTable
                    if self.table.valid_raise_amts[0] > self.table.valid_raise_amts[1]:
                        self.table.valid_raise_amts[0] = self.table.valid_raise_amts[1]

                    if self.table.stage == 0:
                        self.table.stage = 1

                    if self.table.last_decision == "Start":
                        self.table.last_decision = None

                    # send game json here
                    print(self.table)
                    sys.stdout.flush()
                    return False

                assert self.table.last_decision != "Start", "Something went wrong"
                flag = True
                action = self.table.last_decision

                if action == 'Call':
                    call_amt = self.table.to_go - action_player.chipsOnTable
                    call_amt_adj = min(call_amt, action_player.stack)
                    action_player.put_in_chips(call_amt_adj)
                    self.table.onTable += call_amt_adj
                elif action[:5] == 'Raise':
                    raise_amt = int(action[6:])
                    net_amt = raise_amt - action_player.chipsOnTable
                    action_player.put_in_chips(net_amt)
                    self.table.onTable += net_amt
                    self.table.valid_raise_amts[0] = 2 * \
                        raise_amt - self.table.to_go
                    self.table.to_go = raise_amt
                    self.table.adjust_action_order(action_seat)
                    self.table.action_index = 0
                elif action == 'Fold':
                    self.table.action_order.remove(action_seat)
                    action_player.next_round()
                    self.table.action_index -= 1
                    self.table.take_player_cards(action_player)
                elif action == 'Check':
                    pass
                else:
                    raise Exception("invalid move")

            self.table.action_index += 1

        for seat in self.table.action_order:
            self.table.players[seat].next_round()

        self.table.pot += self.table.onTable
        self.table.onTable = 0
        self.table.stage = (self.table.stage + 1) % 6
        self.table.last_decision = "Start"

        return True

    def winner_index(self):
        if len(self.table.action_order) == 1:
            return self.table.action_order[0]
        return None

    def winner_order(self):
        board = self.table.board
        values = {}
        myEvaluator = Evaluator()
        for i, seat in enumerate(self.table.action_order):
            p = self.table.players[seat]
            hand_strength = myEvaluator.evaluate(p.cards, board)
            values.setdefault(hand_strength, []).append(p)

        keys = sorted(list(values.keys()))

        player_ordering = []
        for key in keys:
            player_ordering.append(values[key])

        return player_ordering

    def distribute_pot(self, winners):
        '''
            Assumes that all chips in play have been committed
        '''
        total_commitments = [
            p.committed if p is not None else 0 for p in self.table.players]

        for w in winners:
            num_tied = len(w)
            w.sort(key=lambda x: x.committed)
            for i, p in enumerate(w):
                for j in range(len(total_commitments)):
                    split = int(
                        min(total_commitments[j], p.committed) / (num_tied - i))
                    p.stack += split
                    total_commitments[j] -= split

            if sum(total_commitments) == 0:
                break

        assert sum(total_commitments) == 0, "Pot was distributed incorrectly"

        for p in self.table.players:
            if p is not None:
                p.committed = 0

    def reset_table(self):
        self.table.stage = 0
        self.table.last_decision = "Start"
        self.table.take_players_cards()
        self.table.board = []
        self.table.pot = 0
        self.turn = -1
        self.play_hand()

    def play_hand(self):
        if self.table.stage == 0:
            self.table.set_preflop_action_order()
            self.has_min_players()
            self.move_buttons()
            self.table.deck.shuffle()
            self.deal()
            self.preflop()
            self.round_of_action()
            return

        if self.table.stage == 1:
            finished = self.round_of_action()
            if not finished:
                return

            # preflop winner
            w_pre = self.winner_index()
            if w_pre is not None:
                self.distribute_pot([[self.table.players[w_pre]]])
                self.reset_table()
                return

            self.deal_flop()
            self.table.set_postflop_action_order()
            self.post_flop()

        if self.table.stage == 2:
            finished = self.round_of_action()
            if not finished:
                return

            # postflop winner
            w_post = self.winner_index()
            if w_post is not None:
                self.distribute_pot([[self.table.players[w_post]]])
                self.reset_table()
                return

            self.deal_turn()
            self.table.set_postflop_action_order()
            self.post_flop()

        if self.table.stage == 3:
            finished = self.round_of_action()
            if not finished:
                return

            # postturn winner
            w_turn = self.winner_index()
            if w_turn is not None:
                self.distribute_pot([[self.table.players[w_turn]]])
                self.reset_table()
                return

            self.deal_river()
            self.table.set_postflop_action_order()
            self.post_flop()

        if self.table.stage == 4:
            finished = self.round_of_action()
            if not finished:
                return
            # postriver winner
            w_river = self.winner_index()
            if w_river is not None:
                self.distribute_pot([[self.table.players[w_river]]])
                self.reset_table()
                return

            # showdown winner order
            winners = self.winner_order()
            self.distribute_pot(winners)
            self.reset_table()
            return

    def play_hands(self):
        while True:
            self.play_hand()

    @staticmethod
    def load_game_state(game_state, last_decision):
        t = Table(**game_state)
        t.last_decision = last_decision
        return Game(t)
