import numpy as np
import json


cards = [ [-2] * 5, [-1] * 10, [0] * 15 , [1] * 10 , [2] * 10 , [3] * 10 , [4] * 10 , [5] * 10 , [6] * 10 ,
          [7] * 10 , [8] * 10 , [9] * 10 , [10] * 10 , [11] * 10 , [12] * 10]
cards = [item for sublist in cards for item in sublist]

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


class Skyjo:

    '''
    Skyjo game with single player.

    First must need to `deal_hand` method which spawns your hand with 12 cards of which, two are open.
    A turn starts by updating the card on the table `_update_table`, the initial update will spawn a card on the table.

    There are 2 possible actions:
    1) `action_replace`: Take from table card to replace own card at index i. Will lead to `_update_table`.
    2) Update Table -> Leads to a new card on the table. This will lead to 1) or 3).
    3) `action_open`: Opens card i without taking the card from the table
    '''

    def __init__(self):

        self.cards = cards
        self.n_cards = len(self.cards)
        self.hand = []
        self.states = []
        self.table = []
        self.finished = []
        print(f"There are {self.n_cards} cards in the deck.")

    def _deal(self, n):

        h = np.random.choice(self.cards, n, replace=False)
        print(f"Dealing {n} cards.")
        self._update_deck(h)
        return h

    def _update_deck(self, hand):

        for H in hand:
            self.cards.remove(H)
        self.n_cards = len(self.cards)
        print(f"Updating cards, there are {self.n_cards} left.")
        if self.n_cards < 1:
            self.finished = True
            print("Game finished because no more cards left.")

    def _update_table(self):

        print('Updating table.')
        self.table = self._deal(1)

    def deal_hand(self):

        print("Starting game.")
        self.hand = self._deal(12)
        self.states = [False] * 12 # False is Closed
        self.states[0] = True
        self.states[1] = True
        self.finished = False

    def open_cards(self):
        print(f"Open cards are { self.hand[ self.states ] }")

    def closed_cards(self):

        closed = [i for i, x in enumerate(self.states) if not x]
        if closed is []:
            self.finished = True
            print("Game finished all hand is open.")
        return closed

    def action_replace(self, position):

        print(f"Action: Replacing card at position {position} with {self.table[0]}")
        dummy = self.hand[position]
        self.hand[position] = self.table[0]
        self.table[0] = dummy
        self.states[position] = True

        if len(self.closed_cards()) == 0:
            self.finished = True

    def action_open(self, position):

        print(f"Action: Open card at position {position}, it is a {self.hand[position]}")
        self.states[position] = True

        if len(self.closed_cards()) == 0:
            self.finished = True

    # def list_choices(self):
    #
    #     text = "your possible end-points are\n" \
    #            "(0) /open_card/N" \
    #            " Open a closed card where N is the index of the card." \
    #            "(1) /take_table/N\n " \
    #            " Where N is the index of the card you want to replace.\n" \
    #            "(2) /update_table\n" \
    #            "(3) /take_table/N"

        # return text



    def game_summary(self):
        jsonStr = json.dumps(self.__dict__, indent=4, sort_keys=True, cls=NumpyEncoder)
        return jsonStr



    # def my_hand(self):
    #     message = f"This is my hand: {self.hand[self.states]}, it sums to {np.sum(self.hand[self.states])} and there are {len(self.closed_states())} closed cards."
    #     print(message)
    #     return message







class PlayerRandom:

    def __init__(self, game):
        self.game = game


if __name__ == '__main__':

    s = Skyjo()
    s.game_summary()
    s.return_state()
    # s.open(2)
    # s.game_summary()
    # turn = 0
    # while s.finished is False:
    #     print(f"======Turn {turn}")
    #     s.update_table()
    #     closed_index = s.closed_states()
    #     s.replace(closed_index[0], s.table[0])
    #     s.game_summary()
    #     turn += 1

