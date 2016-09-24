import kivy
from kivy.app import App
from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.logger import Logger
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from gameclasses_v3_0 import GameMaster

from kivy.properties import BoundedNumericProperty, ListProperty, ObjectProperty
from gameclasses_v3_0 import *

kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')

Logger.info('title: This is a info message.')
Logger.debug('title: This is a debug message.')


class ElectionsGame(FloatLayout):
    """This class represents the game. As a Kivy object it represents the game field and is a root for all other
    objects. As a general class it stores all the stuff in the game.
    """
    #deck = ObjectProperty(None)
    gameMaster = GameMaster(1) ##round_id
    #playerTrump = ObjectProperty(Player(player_id=0, swing=0, partisans=0, news=0, hype=0, cash=0, media=1, mojo=1, money=1))
    #playerHillary = ObjectProperty(Player(player_id=1, swing=0, partisans=0, news=0, hype=0, cash=0, media=1, mojo=1, money=1))

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        #self.add_widget(PlayerKv())

class ElectionsApp(App):
    def build(self):
        game = ElectionsGame()
        return game


if __name__ == '__main__':
    ElectionsApp().run()
