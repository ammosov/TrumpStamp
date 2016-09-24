import kivy
import pandas as pd
from kivy.uix.floatlayout import FloatLayout
from card import Card, Cards
from kivy.logger import Logger
kivy.require('1.7.2')


class Hand():
	def __init__(self, player, deck):
		self.player = player
		self.deck = deck
		self.cards = [0] * 6

	def refill(self):  # checks for blanks and replaces them with valid Cards
		for i in range(6):
			if self.cards[i] == 0:
				self.cards[i] = self.deck.pop_card()