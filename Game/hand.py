import os
from kivy.logger import Logger

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class Hand():
    POSITIONS_X = {0: list(map(lambda x: x / 2048.0, [522, 790, 1058, 1326, 1594, 1862])),
    				1: list(map(lambda x: x / 2048.0, [182, 450, 718, 986, 1254, 1522]))}
    POSITIONS_Y = {0: (1536.0 - 1488.0) / 1536.0,
                   1: (1536.0 - 150.0) / 1536.0}

    def __init__(self, deck):
        self.deck = deck
        self.player = deck.get_owner()
        self.cards = [None] * 6

    def pop_card(self, popped_card):
        for i in xrange(len(self.cards)):
            if self.cards[i] == popped_card:
                self.cards[i] = None
    """
    def render_cards(self):
        for i, card in enumerate(self.cards):
            card.pos_hint = {'x': self.POSITIONS_X[self.player.player_id][i],
                             'y': self.POSITIONS_Y[self.player.player_id]}
            card.render()
    """

    def render_cards(self):
        for i, card in enumerate(self.cards):
            if self.player.active:
                card.show()
            else:
                card.hide()
            pos_hint = {'center_x': self.POSITIONS_X[self.player.player_id][i]}
            if self.player.player_id == 1:
                pos_hint['top'] = self.POSITIONS_Y[1]
            else:
                pos_hint['y'] = self.POSITIONS_Y[0]
            card.pos_hint = pos_hint
            card.render()

    def refill(self):
        for i in xrange(len(self.cards)):
            if not self.cards[i]:
                new_card  = self.deck.pop_card()
                self.cards[i] = new_card
