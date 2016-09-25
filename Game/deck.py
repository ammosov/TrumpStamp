import kivy
from kivy.uix.floatlayout import FloatLayout
from card import Card, CardFabric
from kivy.logger import Logger
import random
kivy.require('1.7.2')


class Deck():
    def __init__(self, player, card_fabric):
        self.player = player
        self.cards = [card_fabric.get_card(i, player.get_player_id()) for i in xrange(1, 54)]
        self.discard = []

    def get_owner(self):
        return self.player

    def shuffle(self):
        random.shuffle(self.cards)

    def pop_card(self):
        if len(self.cards) == 0:
            self.cards = self.discard
            self.discard = []
            self.shuffle()
        return self.cards.pop()


    def drop_card(self, card):
    	# played cards should be in discard too
    	self.discard.append(card)
