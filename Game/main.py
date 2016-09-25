import kivy
import kwad
from kivy.app import App
from kivy.config import Config
from elections_game import ElectionsGame
from kivy.uix.screenmanager import ScreenManager
from start_screen import StartScreen

kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')

class ElectionsApp(App):
    start_screen_name = "startscreen"
    game_screen_name = "electionsgame"

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(sm, name=self.start_screen_name))
        sm.add_widget(ElectionsGame(name=self.game_screen_name))
        return sm


if __name__ == '__main__':
    kwad.attach()
    ElectionsApp().run()
