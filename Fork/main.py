import kivy
import kwad
from kivy.app import App
from kivy.config import Config
from elections_game import ElectionsGame

kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')


class ElectionsApp(App):
    def build(self):
        return ElectionsGame()


if __name__ == '__main__':
    kwad.attach()
    ElectionsApp().run()
