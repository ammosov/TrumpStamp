import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from kivy.properties import BoundedNumericProperty, ListProperty, ObjectProperty

kivy.require('1.9.1')
Config.set('kivy', 'log_level', 'debug')

Logger.info('title: This is a info message.')
Logger.debug('title: This is a debug message.')


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
