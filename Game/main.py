import kivy
import kwad
from kivy.app import App
from kivy.config import Config
from elections_game import ElectionsGame
from kivy.uix.screenmanager import ScreenManager
from start_screen import StartScreen
from kivy.core.window import Window
from kivy.utils import platform


kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')


class ElectionsApp(App):
    start_screen_name = "startscreen"
    game_screen_name = "electionsgame"

    def build(self):
        sm = ScreenManager()
        start_screen = StartScreen(sm, name=self.start_screen_name)
        return sm


if __name__ == '__main__':
    kwad.attach()
    if platform not in ('linux', 'windows', 'macosx'):
        Window.rotation = -90
    ElectionsApp().run()
