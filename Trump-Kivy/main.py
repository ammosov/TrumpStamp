import kivy

from kivy.config import Config
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import BoundedNumericProperty, ListProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.logger import Logger

import csv

kivy.require('1.9.1')
Config.set('kivy', 'log_level', 'debug')

Logger.info('title: This is a info message.')
Logger.debug('title: This is a debug message.')


class TrumpAssetStorage(object):
    def __init__(self):
        print("bla")
        # cards_address = 'assets' + os.path.sep + 'cards'
        # Logger.debug("TrumpApp: Cards address: %s", cards_address)
        # list_file = cards_address + os.path.sep + 'DECK_1_4.csv'
        list_file = 'cards.csv'
        Logger.debug("TrumpApp: Csv file loading: %s", list_file)
        with open(list_file) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for row in reader:
                pass
                # print('Loaded card: trump:', row['trump'], 'hillary:', row['hillary'])


class Card(Button, Widget):
    """" This is a GUI class, representing a game field object."""
    myWavSound = SoundLoader.load('assets/stubs/Sounds/card.wav')
    background_normal = 'assets/cards/hillary/101.png'

    def play_card(self):
        # self.parent.scoreTrump += 1
        self.myWavSound.play()


class Player(Widget):
    partisans = BoundedNumericProperty(0, min=0, max=125, rebind=True)
    swing_voters = BoundedNumericProperty(0, min=0, rebind=True)

    media = BoundedNumericProperty(1, min=1, max=100)
    news = BoundedNumericProperty(1, min=0, max=300)
    mojo = BoundedNumericProperty(1, min=1, max=100)
    charisma = BoundedNumericProperty(1, min=0, max=300)
    donors = BoundedNumericProperty(1, min=1, max=100)
    cash = BoundedNumericProperty(1, min=0, max=300)

    cards_actions = ListProperty()  # Should have a list of card actions


class ElectionsGame(FloatLayout):
    """This class represents the game. As a Kivy object it represents the game field and is a root for all other
    objects. As a general class it stores all the stuff in the game.
    """
    deck = ObjectProperty(None)
    playerTrump = ObjectProperty(Player)
    playerHillary = ObjectProperty(Player)


class ElectionsApp(App):
    def build(self):
        game = ElectionsGame()
        return game


if __name__ == '__main__':
    ElectionsApp().run()
