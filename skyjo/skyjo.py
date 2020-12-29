import numpy as np
import json


cards = [ [-2] * 5, [-1] * 10, [0] * 15 , [1] * 10 , [2] * 10 , [3] * 10 , [4] * 10 , [5] * 10 , [6] * 10 ,
          [7] * 10 , [8] * 10 , [9] * 10 , [10] * 10 , [11] * 10 , [12] * 10]
cards = [item for sublist in cards for item in sublist]

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return obj.tolist()
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if callable(obj):
            return obj.__name__
        return json.JSONEncoder.default(self, obj)


class Skyjo:

    '''
    Skyjo game with single player.

    First one must need to `deal_hand` method which spawns your hand with 12 cards of which, two are open.
    A turn starts by updating the card on the table `_update_table`, the initial update will spawn a card
    on the table.

    There are 2 possible actions:

    1) `action_replace`: Take from table card to replace own card at index i. Will lead to `_update_table`.
    2) `action_open`: Opens card i without taking the card from the table
    '''

    def __init__(self):

        self.deck = []
        self.deck_size = []
        self.hand = []
        self.states = []
        self.table = []
        self.finished = []
        self.possible_actions = [self.start_game]
        print(f"There are {self.deck_size} cards in the deck.")

    def _deal(self, n):

        h = np.random.choice(self.deck, n, replace=False)
        print(f"Dealing {n} cards.")
        self._update_deck(h)
        return h

    def _update_deck(self, hand):

        for H in hand:
            self.deck.remove(H)
        self.deck_size = len(self.deck)
        print(f"Updating cards, there are {self.deck_size} left.")
        if self.deck_size < 1:
            self.finished = True
            print("Game finished because no more cards left.")

    def deal_hand(self):
        """
        Deals a hand of 12 cards with 2 open ones.
        """
        print("Starting game.")
        self.hand = self._deal(12)
        self.states = [False] * 12  # False is Closed
        self.states[0] = True
        self.states[1] = True

    def start_game(self):

        self.deck = cards
        self.deck_size = len(self.deck)
        self.deal_hand()
        self._deck_to_table()
        self.possible_actions = [self._hand_table_exchange, self._deck_to_table]
        self.finished = False
        return self.game_summary()

    def _hand_table_exchange(self, position):

        print(f"Action: Replacing card at position {position} with {self.table}")
        dummy = self.hand[position]
        self.hand[position] = self.table.pop(-1)
        self.table.extend([dummy])
        self._open_card(position)
        self.possible_actions = [self._hand_table_exchange, self._deck_to_table]

        if len(self.closed_cards()) == 0:
            self.finished = True
            self.possible_actions = None

        return self.game_summary()

    def _deck_to_table(self):

        card = self._deal(1)
        print(f"Moving card {card} from deck to table.")
        self.table.extend(card)
        self.possible_actions = [self._hand_table_exchange, self._open_card]

        return self.game_summary()

    def _open_card(self, position):

        print(f"Action: Open card at position {position}, it is a {self.hand[position]}")
        self.states[position] = True

        if len(self.closed_cards()) == 0:
            self.finished = True

        return self.game_summary()

    def closed_cards(self):

        closed = [i for i, x in enumerate(self.states) if not x]
        if closed is []:
            self.finished = True
            print("Game finished all hand is open.")
        return closed

    def game_summary(self):
        print('Game Summary:')
        jsonStr = json.dumps(self.__dict__, indent=4, sort_keys=True, cls=NumpyEncoder)
        print(jsonStr)
        return jsonStr


if __name__ == '__main__':

    s = Skyjo()
    s.game_summary()
    s.start_game()
    s.game_summary()
    s._deck_to_table()
    s.game_summary()
    s._hand_table_exchange(3)
    s.game_summary()
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

