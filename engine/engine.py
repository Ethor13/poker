from deck import Deck


class Engine:

    def __init__(self, board, hands):
        self.board = board
        self.hands = hands

    def sort_by_value(all_cards):
        all_cards.sort(reverse=True)

    def sort_by_suit(all_cards):
        all_cards.sort(key=lambda x: x[1])

    # all hand eval functions assume all_cards is sorted in descending order
    def high_card(all_cards):
        return all_cards[:5]

    def pair(all_cards):
        for i in range(len(all_cards) - 1):
            if all_cards[i][0] == all_cards[i+1][0]:
                pair = all_cards[i:i+2]
                temp = all_cards.copy()
                del temp[i:i+2]
                return pair + temp[:3]
        return None

    def two_pair(all_cards):
        for i in range(len(all_cards) - 3):
            if all_cards[i][0] == all_cards[i+1][0]:
                for j in range(i+2, len(all_cards)-1):
                    if all_cards[j][0] == all_cards[j+1][0]:
                        pair1 = all_cards[i:i+2]
                        pair2 = all_cards[j:j+2]
                        temp = all_cards.copy()
                        del temp[j:j+2]
                        del temp[i:i+2]
                        return pair1 + pair2 + temp[:1]
        return None

    def three_of_a_kind(all_cards):
        for i in range(len(all_cards) - 2):
            if all_cards[i][0] == all_cards[i+1][0] and all_cards[i][0] == all_cards[i+2][0]:
                trips = all_cards[i:i+3]
                temp = all_cards.copy()
                del temp[i:i+3]
                return trips + temp[:2]
        return None

    def straight(all_cards):
        temp = [all_cards[0]]
        for i in range(1, len(all_cards)):
            if all_cards[i][0] != temp[len(temp) - 1][0]:
                temp.append(all_cards[i])

        for i in range(len(temp) - 3):
            if temp[i][0] == temp[i+1][0] + 1 and \
                    temp[i+1][0] == temp[i+2][0] + 1 and \
                    temp[i+2][0] == temp[i+3][0] + 1:
                if len(temp) > i + 4 and temp[i+3][0] == temp[i+4][0] + 1:
                    return temp[i:i+5]
                elif temp[i+3][0] == 2 and temp[0][0] == 14:
                    return temp[i:i+4] + temp[:1]
        return None

    def flush(all_cards):
        temp = all_cards.copy()
        Engine.sort_by_suit(temp)
        for i in range(len(all_cards) - 4):
            if temp[i][1] == temp[i+4][1]:
                return temp[i:i+5]
        return None

    def full_house(all_cards):
        for i in range(len(all_cards) - 2):
            if all_cards[i][0] == all_cards[i+1][0] and all_cards[i][0] == all_cards[i+2][0]:
                trips = all_cards[i:i+3]
                temp = all_cards.copy()
                del temp[i:i+3]
                for j in range(len(temp) - 1):
                    if temp[j][0] == temp[j+1][0]:
                        return trips + temp[j:j+2]
        return None

    def four_of_a_kind(all_cards):
        for i in range(len(all_cards) - 3):
            if all_cards[i][0] == all_cards[i+3][0]:
                quads = all_cards[i:i+4]
                if i == 0:
                    return quads + all_cards[4:5]
                else:
                    return quads + all_cards[:1]

    def straight_flush(all_cards):
        temp = all_cards.copy()
        Engine.sort_by_suit(temp)
        for i in range(len(temp) - 4):
            for j in range(len(temp)-1, i+3, -1):
                if temp[i][1] == temp[j][1]:
                    return Engine.straight(temp[i:j+1])
        return None

    def royal_flush(all_cards):
        sf = Engine.straight_flush(all_cards)
        if sf is not None and sf[0][0] == 14:
            return sf
        return None

    def eval_hand(all_cards):
        temp = all_cards.copy()
        Engine.sort_by_value(temp)
        rf = Engine.royal_flush(temp)
        if rf is not None:
            return (10, rf)
        sf = Engine.straight_flush(temp)
        if sf is not None:
            return (9, sf)
        four = Engine.four_of_a_kind(temp)
        if four is not None:
            return (8, four)
        full = Engine.full_house(temp)
        if full is not None:
            return (7, full)
        flush = Engine.flush(temp)
        if flush is not None:
            return (6, flush)
        straight = Engine.straight(temp)
        if straight is not None:
            return (5, straight)
        three = Engine.three_of_a_kind(temp)
        if three is not None:
            return (4, three)
        two_pair = Engine.two_pair(temp)
        if two_pair is not None:
            return (3, two_pair)
        pair = Engine.pair(temp)
        if pair is not None:
            return (2, pair)
        return (1, Engine.high_card(temp))

    def compare_hands(hands):
        temp = hands.copy()
        temp.sort(reverse=True)
        # finish this
