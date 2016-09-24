import kivy
import pandas as pd
from kivy.uix.floatlayout import FloatLayout
from card import Card, Cards
from kivy.logger import Logger
kivy.require('1.7.2')


class Hand():
	def __init__(self, player):
		self.player = player
		