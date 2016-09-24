import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout

from card import *

kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')


class ElectionsGame(FloatLayout):
    """This class represents the game. As a Kivy object it represents the game field and is a root for all other
    objects. As a general class it stores all the stuff in the game.
    """
    # deck = ObjectProperty(None)
    # playerTrump = ObjectProperty(Player(player_id=0, swing=0, partisans=0, news=0, hype=0, cash=0, media=1, mojo=1))
    # playerHillary = ObjectProperty(Player(player_id=1, swing=0, partisans=0, news=0, hype=0, cash=0, media=1, mojo=1))

    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        self.ids['PlayerTrump'].late_init(player_id=0, swing=0, partisans=100, news=0, hype=0, cash=0, media=1, mojo=1)
        # self.game_master = GameMaster(0)


class ElectionsApp(App):
    def build(self):
        game = ElectionsGame()
        return game


if __name__ == '__main__':
    ElectionsApp().run()
