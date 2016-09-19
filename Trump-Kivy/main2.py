import kivy
kivy.require('1.9.1')
from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import BoundedNumericProperty, ReferenceListProperty,\
    ObjectProperty, ListProperty
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader

import csv
import os.path
# import logging
from kivy.logger import Logger
Logger.info('title: This is a info message.')
Logger.debug('title: This is a debug message.')


class TrumpAssetStorage(object):

    def __init__(self):
        print( "bla")
        # cards_address = 'assets' + os.path.sep + 'cards'
        # Logger.debug("TrumpApp: Cards address: %s", cards_address)
        # listfile = cards_address + os.path.sep + 'DECK_1_4.csv'
        listfile = 'cards.csv'
        Logger.debug( "TrumpApp: Csv file loading: %s", listfile)
        with open( listfile ) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                pass
                # print('Loaded card: trump:', row['trump'], 'hillary:', row['hillary'])


class TrumpCard( Button ):
    """" This is a GUI class, representing a game field object."""
    myWavSound = SoundLoader.load('assets/stubs/Sounds/card.wav')
    background_normal = 'assets/cards/hillary/101.png'

    def play_card(self):

        # self.parent.scoreTrump += 1
        self.myWavSound.play()


class TrumpPlayer(Widget):
    partisans = BoundedNumericProperty(0, min=0, max=125, rebind=True)
    swing_voters = BoundedNumericProperty(0, min=0)

    media = BoundedNumericProperty(1, min=1, max=100)
    news = BoundedNumericProperty(1, min=0, max=300)
    mojo = BoundedNumericProperty(1, min=1, max=100)
    charisma = BoundedNumericProperty(1, min=0, max=300)
    donors = BoundedNumericProperty(1, min=1, max=100)
    cash = BoundedNumericProperty(1, min=0, max=300)

    cards_actions = ListProperty([])  # Should have a list of card actions


class TrumpPlayerTrump(TrumpPlayer):
    pass


class TrumpPlayerHillary(TrumpPlayer):
    pass


class TrumpGame(FloatLayout):
    """This class represents the game. As a Kivy object it represents the game field and is a root for all other
    objects. As a general class it stores all the stuff in the game.
    """
    myPlayerTrump = TrumpPlayerTrump()
    myPlayerHillary = TrumpPlayerHillary()
    myAssetStorage = TrumpAssetStorage()


class TrumpApp(App):
    def build(self):
        game = TrumpGame()
        return game

if __name__ == '__main__':
    TrumpApp().run()
