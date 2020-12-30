import numpy as np
import json
from pprint import pprint as pp

# all cards of the game
cards = [ [-2] * 5, [-1] * 10, [0] * 15 , [1] * 10 , [2] * 10 , [3] * 10 , [4] * 10 , [5] * 10 , [6] * 10 ,
          [7] * 10 , [8] * 10 , [9] * 10 , [10] * 10 , [11] * 10 , [12] * 10]
# flatten the list of lists
cards = [item for sublist in cards for item in sublist]

class NumpyEncoder(json.JSONEncoder):
    # Custom encoder to convert dict to json
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

    First one must need to `start_game` which spawns your hand with 12 cards of which, two are open.
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
        self.states = [False] * 12
        self.table = []
        self.finished = []
        self.possible_actions = [self.start_game]
        # self.masked_hand = masked_hand
        print(f"There are {self.deck_size} cards in the deck.")

    @property
    def points(self):
        # Current points of the hand.

        if len(self.hand) != 0:
            return np.sum(self.hand[self.states])

    @property
    def masked_hand(self):
        # hand with opened cards.

        masked_hand = ['*'] * 12
        for i in range(12):
            if self.states[i] is True:
                masked_hand[i] = str(self.hand[i])
        return masked_hand

    def _deal(self, n):
        # Internal function to move cards from the deck to hand or to table.

        h = np.random.choice(self.deck, n, replace=False)
        print(f"Dealing {n} cards.")
        self._update_deck(h)
        return h

    def _update_deck(self, hand):
        # removes dealt cards from the deck

        for H in hand:
            self.deck.remove(H)
        self.deck_size = len(self.deck)
        print(f"Updating cards, there are {self.deck_size} left.")

    def _deal_hand(self):
        """
        Deals a hand of 12 cards with 2 open ones.
        """
        self.hand = self._deal(12)
        # TODO: Organize in triplets
        self.states = [False] * 12  # False is Closed
        self.states[0] = True
        self.states[1] = True

    def start_game(self):
        # Gets a deck, and deals 1 card to table and 12 cards to a hand.

        print("Starting game.")
        self.deck = cards
        self.deck_size = len(self.deck)
        self._deal_hand()
        self.update_table()
        self.possible_actions = [self.exchange_card, self.update_table]
        self.finished = False
        return self.summary()

    def exchange_card(self, position):
        # Exchanges the card at position with the one on the table (and opens it).

        print(f"Action: Replacing card at position {position} with {self.table}")
        dummy = self.hand[position]
        self.hand[position] = self.table.pop(-1)
        self.open_card(position)

        self.table.extend([dummy])
        self.possible_actions = [self.exchange_card, self.update_table]
        return self.summary()

    def update_table(self):

        card = self._deal(1)
        print(f"Moving card {card} from deck to table.")
        self.table.extend(card)
        self.possible_actions = [self.exchange_card, self.open_card]
        self.game_checks()
        return self.summary()

    def open_card(self, position):

        print(f"Action: Open card at position {position}, it is a {self.hand[position]}")
        self.states[position] = True
        self.game_checks()

    def game_checks(self):

        # if there are no more cards in the deck
        if self.deck_size < 1:
            self.finished = True
            print("Game finished because no more cards left.")
            self.possible_actions = None

        # if all cards are open
        if len(self.closed_cards()) == 0:
            self.finished = True
            self.possible_actions = None

        if self.finished is True:
            self.possible_actions = [self.start_game]

        return self.summary()

    def closed_cards(self):

        closed = [i for i, x in enumerate(self.states) if not x]
        if closed is []:
            self.finished = True
            print("Game finished all hand is open.")
        return closed

    def summary(self):

        if self.finished is False:
            merged = {**json.loads(self.user_summary()), **json.loads(self.game_summary())}
            print(json.dumps(merged, indent=4, sort_keys=True, cls=NumpyEncoder))
        else:
            merged = {**json.loads(self.end_summary())}
            print(json.dumps(merged, indent=4, sort_keys=True, cls=NumpyEncoder))

        return merged

    def end_summary(self):
        include = ['hand', 'finished']
        user_dict = {k: self.__dict__[k] for k in include}
        user_dict['points'] = self.points
        jsonStr = json.dumps({"endgame_summary": user_dict}, indent=4, sort_keys=True, cls=NumpyEncoder)
        return jsonStr

    def user_summary(self):
        include = ['table', 'possible_actions', 'finished']
        user_dict = {k:self.__dict__[k] for k in include}
        user_dict['points'] = self.points
        user_dict['masked_hand'] = self.masked_hand
        jsonStr = json.dumps({"user_summary":user_dict}, indent=4, sort_keys=True, cls=NumpyEncoder)
        return jsonStr

    def game_summary(self):
        summary = self.__dict__
        summary.pop('deck', None)
        jsonStr = json.dumps({"game_summary" : summary}, indent=4, sort_keys=True, cls=NumpyEncoder)
        return jsonStr


if __name__ == '__main__':

    s = Skyjo()
    s.summary()
    s.start_game()
    s.summary()

    while s.finished is False:
        s.update_table()
        s.summary()



