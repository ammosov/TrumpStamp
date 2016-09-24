import kivy
import pandas as pd
from kivy.uix.floatlayout import FloatLayout
from card import Card, Cards
from kivy.logger import Logger
import random
kivy.require('1.7.2')


class Deck():
	
	def __init__(self, player):
		self.player = player
		self.cards = [1, 2, 3, 4]

	def shuffle(self):
		random.shuffle(self.cards)