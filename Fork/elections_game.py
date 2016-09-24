import kivy
from kivy.uix.floatlayout import FloatLayout
from game_master import GameMaster
kivy.require('1.7.2')


class ElectionsGame(FloatLayout):
    """This class represents the game. As a Kivy object it represents the game field and is a root for all other
    objects. As a general class it stores all the stuff in the game.
    """
    def __init__(self, **kwargs):
        super(FloatLayout, self).__init__(**kwargs)
        gameMaster = GameMaster(self.ids['PlayerTrump'], self.ids['PlayerHillary'], self)
