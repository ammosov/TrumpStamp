import kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.floatlayout import FloatLayout
from card import Card, CardFabric
from elections_game import ElectionsGame

kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')


class ElectionsApp(App):
    def build(self):
        game = ElectionsGame()
        return game


if __name__ == '__main__':
    ElectionsApp().run()
