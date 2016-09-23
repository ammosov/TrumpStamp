import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from kivy.properties import BoundedNumericProperty, ListProperty, ObjectProperty
from gameclasses_v3_0 import *

kivy.require('1.9.1')
Config.set('kivy', 'log_level', 'debug')

Logger.info('title: This is a info message.')
Logger.debug('title: This is a debug message.')


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
