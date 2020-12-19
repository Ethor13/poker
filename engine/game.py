from table import Table
from engine import Engine


class Game:

    def __init__(self, table):
        self.table = table

    def has_min_players(self, minimum=2):
        if self.table.get_num_players() < minimum:
            raise Exception("Not enough players")

    def move_buttons(self):
        dealer_index = (self.table.get_dealer() + 1) % self.table.max_players
        while self.table.get_player(dealer_index) is None or self.table.get_player_chips(dealer_index) == 0:
            dealer_index = (dealer_index + 1) % self.table.max_players
        self.table.set_dealer(dealer_index)

        sb_index = (self.table.get_dealer() + 1) % self.table.max_players
        while self.table.get_player(sb_index) is None or self.table.get_player_chips(sb_index) == 0:
            sb_index = (sb_index + 1) % self.table.max_players
        self.table.set_sb(sb_index)

        bb_index = (self.table.get_sb() + 1) % self.table.max_players
        while self.table.get_player(bb_index) is None or self.table.get_player_chips(bb_index) == 0:
            bb_index = (bb_index + 1) % self.table.max_players
        self.table.set_bb(bb_index)

    def deal(self):
        for _ in range(2):
            for p in self.table.get_players():
                if p is not None and p.get_chips() > 0:
                    p.add_card(self.table.deck.deal_card())

    def preflop(self):
        involved = [False if p is None or p.get_chips(
        ) == 0 else True for p in self.table.get_players()]

        commitment = [0] * self.table.max_players
        sb_amt = min(self.table.get_blinds()[
                     0], self.table.get_player_chips(self.table.get_sb()))
        commitment[self.table.get_sb()] = sb_amt
        self.table.get_player(self.table.get_sb()).subtract_chips(sb_amt)
        bb_amt = min(self.table.get_blinds()[
                     1], self.table.get_player_chips(self.table.get_bb()))
        commitment[self.table.get_bb()] = bb_amt
        self.table.get_player(self.table.get_bb()).subtract_chips(bb_amt)

        # Under the Gun
        action = (self.table.get_bb() + 1) % self.table.max_players
        # Big Blind
        last_to_act = self.table.get_bb()
        to_play = self.table.get_blinds()[1]

        return self.round_of_action(involved, commitment, action, last_to_act, to_play)

    def deal_flop(self):
        for i in range(3):
            self.table.set_board_card(i, self.table.deck.deal_card())
        print(self.table.get_board())

    def deal_turn(self):
        self.table.set_board_card(3, self.table.deck.deal_card())
        print(self.table.get_board())

    def deal_river(self):
        self.table.set_board_card(4, self.table.deck.deal_card())
        print(self.table.get_board())

    def post_flop(self, involved):
        commitment = [0] * self.table.max_players
        # Left of Dealer
        action = (self.table.get_dealer() + 1) % self.table.max_players
        # Big Blind
        last_to_act = self.table.get_dealer()
        to_play = 0

        return self.round_of_action(involved, commitment, action, last_to_act, to_play)

    def round_of_action(self, involved, commitment, action, last_to_act, to_play):
        count = 0
        for p in self.table.get_players():
            if p is not None and p.get_chips() > 0:
                count += 1
        if count < 2:
            return involved, commitment

        completed = False
        while not completed:
            if involved[action]:
                action_chips = self.table.get_player(action).get_chips()
                if action_chips > 0:
                    flag = True
                    while flag:
                        print(
                            f"It's {self.table.get_player(action).get_name()}'s turn")
                        print(
                            f"Your cards are {self.table.get_player(action).get_cards()}")
                        print(
                            f"It costs {to_play} to play. You would need to put in {to_play - commitment[action]} in the pot. What do you want to do?")
                        response = input()
                        print()

                        if commitment[action] < to_play:
                            if response == 'fold':
                                involved[action] = False
                                flag = False

                            elif response == 'call':
                                to_call = to_play - commitment[action]
                                if action_chips < to_call:
                                    self.table.get_player(
                                        action).subtract_chips(action_chips)
                                    commitment[action] += action_chips
                                else:
                                    self.table.get_player(
                                        action).subtract_chips(to_call)
                                    commitment[action] = to_play
                                flag = False

                        elif commitment[action] == to_play and response == 'check':
                            flag = False

                        if response[:9] == 'raise to ':
                            try:
                                raise_amt = int(response[9:])
                            except ValueError:
                                print("Invalid Raise Amount")
                            if raise_amt > (action_chips + commitment[action]) or raise_amt < (2 * to_play):
                                print("Invalid Raise Amount")
                            else:
                                self.table.get_player(
                                    action).subtract_chips(raise_amt - commitment[action])
                                commitment[action] = raise_amt
                                to_play = raise_amt
                                last_to_act = (
                                    action - 1) % self.table.max_players
                                flag = False

                        if flag:
                            print("Invalid Input")

            if action == last_to_act:
                completed = True
            action = (action + 1) % self.table.max_players

        return involved, commitment

    def winner_index(involved):
        count = 0
        for b in involved:
            if b == True:
                count += 1
        if count == 0:
            raise Exception("No Players left in the hand")
        if count == 1:
            return commitment.index(True)
        if count > 1:
            return None

    def sort_player_hands(hands):
        hands_alt = list(
            map(lambda x: (list(map(lambda y: y[0], x[0])), x[1]), hands))
        hands_alt.sort(key=lambda x: x[0])
        player_ordering = []
        while len(hands_alt) > 0:
            h = hands_alt[0][0]
            last_match = 0
            while last_match + 1 < len(hands_alt) and h == hands_alt[last_match + 1][0]:
                last_match += 1
            players = list(map(lambda x: x[1], hands_alt[:last_match + 1]))
            player_ordering.append(players)
            del hands_alt[:last_match+1]
        return player_ordering

    def winner_order(self, involved):
        board = self.table.get_board()
        hands = []
        for i, p in enumerate(self.table.get_players()):
            if involved[i]:
                hand_strength, hand = Engine.eval_hand(board + p.get_cards())
                hands.append((hand_strength, hand, p))

        # an entry in hand_ordering[i] has a hand_strength of i
        hand_ordering = [[] for _ in range(11)]
        for h in hands:
            hand_ordering[h[0]].append(h[1:])

        # orders the players hands from least to greatest showdown value
        player_ordering = []
        for h in hand_ordering:
            player_ordering += Game.sort_player_hands(h)

        # returns the ordering of players from greatest to least hand value
        player_ordering.reverse()
        return player_ordering

    def distribute_pot(self, winners, total_commitments):
        print("total commitments:", total_commitments)
        for w in winners:
            num_tied = len(w)
            player_commitments = [
                (total_commitments[self.table.get_player_seat(p)], p) for p in w]
            player_commitments.sort(key=lambda x: x[0])
            for i, (_, p) in enumerate(player_commitments):
                for j in range(len(total_commitments)):
                    split = min(total_commitments[j], total_commitments[self.table.get_player_seat(
                        p)]) / (num_tied - i)
                    p.add_chips(split)
                    total_commitments[j] -= split
            if sum(total_commitments) == 0:
                break
        if sum(total_commitments) != 0:
            raise Exception("Pot was distributed incorrectly")

    def play_hand(self):
        self.has_min_players()
        self.move_buttons()
        self.table.reset_board()
        self.table.deck.shuffle()
        self.table.set_pot(0)
        self.deal()
        involved_pre, commitment_pre = self.preflop()
        self.table.add_to_pot(sum(commitment_pre))
        w_pre = Game.winner_index(involved_pre)
        if w_pre is None:
            self.deal_flop()
            involved_post, commitment_post = self.post_flop(involved_pre)
            self.table.add_to_pot(sum(commitment_post))
            w_post = Game.winner_index(involved_post)
            if w_post is None:
                self.deal_turn()
                involved_turn, commitment_turn = self.post_flop(involved_post)
                self.table.add_to_pot(sum(commitment_turn))
                w_turn = Game.winner_index(involved_turn)
                if w_turn is None:
                    self.deal_river()
                    involved_river, commitment_river = self.post_flop(
                        involved_turn)
                    self.table.add_to_pot(sum(commitment_river))
                    w_river = Game.winner_index(involved_river)
                    if w_river is None:
                        # evaluate hands at showdown
                        winners = self.winner_order(involved_river)
                        total_commitments = list(map(
                            sum, zip(commitment_pre, commitment_post, commitment_turn, commitment_river)))
                        self.distribute_pot(winners, total_commitments)
                    else:
                        # river winner before showdown
                        self.table.get_player(w_river).add_chips(
                            self.table.get_pot())
                else:
                    # turn winner
                    self.table.get_player(w_turn).add_chips(
                        self.table.get_pot())
            else:
                # post flop winner
                self.table.get_player(w_post).add_chips(self.table.get_pot())
        else:
            # pre flop winner
            self.table.get_player(w_pre).add_chips(self.table.get_pot())

        self.table.take_player_cards()
