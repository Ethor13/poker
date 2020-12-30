from table import Table
from evaluator import Evaluator
from card import Card


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
        Card.print_pretty_cards(self.table.board)

    def deal_turn(self):
        self.table.board.append(self.table.deck.draw())
        Card.print_pretty_cards(self.table.board)

    def deal_river(self):
        self.table.board.append(self.table.deck.draw())
        Card.print_pretty_cards(self.table.board)

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
        self.table.pot += sb_amt_adj + bb_amt_adj

        to_go = self.table.blinds[1]

        self.round_of_action(to_go)

    def post_flop(self):
        '''
            Assumes set_postflop_action_order has already been called
        '''
        to_go = 0

        self.round_of_action(to_go)

    def round_of_action(self, to_go):
        action_index = 0

        # skip while loop if only one person can make a move
        if self.table.active_players() < 2:
            action_index = len(self.table.action_order)

        while action_index < len(self.table.action_order):
            action_seat = self.table.action_order[action_index]
            action_player = self.table.players[action_seat]
            if action_player.stack > 0:
                while True:
                    print(f"{str(action_player)}'s turn")
                    Card.print_pretty_cards(action_player.cards)
                    action = input("Enter an action: ")
                    print()
                    if action == 'call':
                        if to_go > action_player.chipsOnTable:
                            call_amt = to_go - action_player.chipsOnTable
                            call_amt_adj = min(call_amt, action_player.stack)
                            action_player.put_in_chips(call_amt_adj)
                            self.table.pot += call_amt_adj
                            break
                        print("invalid call")
                    elif action[:5] == 'raise':
                        try:
                            raise_amt = int(action[6:])
                        except:
                            # make the following if statement always fail
                            raise_amt = action_player.chipsOnTable + action_player.stack + 1
                        net_amt = raise_amt - action_player.chipsOnTable
                        if net_amt <= action_player.stack and self.table.active_players() > 1:
                            action_player.put_in_chips(net_amt)
                            self.table.pot += net_amt
                            to_go = raise_amt
                            self.table.adjust_action_order(action_seat)
                            action_index = 0
                            break
                        print("invalid raise")
                    elif action == 'fold':
                        if to_go > action_player.chipsOnTable:
                            self.table.action_order.remove(action_seat)
                            action_player.next_round()
                            action_index -= 1
                            break
                        print("invalid fold")
                    elif action == 'check':
                        if to_go == action_player.chipsOnTable:
                            break
                        print("invalid check")
                    else:
                        print("invaid response")

            action_index += 1

        for seat in self.table.action_order:
            self.table.players[seat].next_round()

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

    def play_hand(self):
        self.table.set_preflop_action_order()
        self.has_min_players()
        self.move_buttons()
        self.table.deck.shuffle()
        self.deal()
        self.preflop()

        while True:
            # preflop winner
            w_pre = self.winner_index()
            if w_pre is not None:
                self.distribute_pot([[self.table.players[w_pre]]])
                break

            self.deal_flop()
            self.table.set_postflop_action_order()
            self.post_flop()

            # postflop winner
            w_post = self.winner_index()
            if w_post is not None:
                self.distribute_pot([[self.table.players[w_post]]])
                break

            self.deal_turn()
            self.table.set_postflop_action_order()
            self.post_flop()
            # postturn winner
            w_turn = self.winner_index()
            if w_turn is not None:
                self.distribute_pot([[self.table.players[w_turn]]])
                break

            self.deal_river()
            self.table.set_postflop_action_order()
            self.post_flop()
            # postriver winner
            w_river = self.winner_index()
            if w_river is not None:
                self.distribute_pot([[self.table.players[w_river]]])
                break

            # showdown winner order
            winners = self.winner_order()
            self.distribute_pot(winners)
            break

        self.table.take_player_cards()
        self.table.board = []
        self.table.pot = 0
