import os
from kivy.logger import Logger

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

class Hand():
    POSITIONS_X = {0: [414 / 2048.0, 682 / 2048.0, 950 / 2048.0, 1218 / 2048.0, 1486 / 2048.0, 1754 / 2048.0], 
    				1: [34 / 2048.0, 302 / 2048.0, 570 / 2048.0, 838 / 2048.0, 1106 / 2048.0, 1374 / 2048.0]}
    POSITIONS_Y = {0: (1536.0 - 1488.0) / 1536.0,
                   1: (1536.0 - 500.0) / 1536.0}

    def __init__(self, deck):
        self.deck = deck
        self.player = deck.get_owner()
        self.cards = [None] * 6

    def pop_card(self, popped_card):
        for i in xrange(len(self.cards)):
            if self.cards[i] == popped_card:
                self.cards[i] = None

    def render_cards(self):
        for i, card in enumerate(self.cards):
            card.pos_hint = {'x': self.POSITIONS_X[self.player.player_id][i],
                             'y': self.POSITIONS_Y[self.player.player_id]}
            card.render()

    def render_cards(self):
        for i, card in enumerate(self.cards):
            if self.player.active:
                card.show()
            else:
                card.hide()
            card.pos_hint = {'x': self.POSITIONS_X[self.player.player_id][i],
                             'y': self.POSITIONS_Y[self.player.player_id]}
            card.render()

    def refill(self):
        for i in xrange(len(self.cards)):
            if not self.cards[i]:
                new_card  = self.deck.pop_card()
                print 'new_card', new_card
                self.cards[i] = new_card
