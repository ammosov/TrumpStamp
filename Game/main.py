"""Main module."""
import kivy
import kwad
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
from start_screen import StartScreen


kivy.require('1.7.2')
Config.set('kivy', 'log_level', 'debug')


class ElectionsApp(App):
    """Main app."""

    start_screen_name = "startscreen"
    end_screen_name = "endscreen"
    game_screen_name = "electionsgame"

    def build(self):
        """Init screen manager."""
        sm = ScreenManager()
        StartScreen(sm, name=self.start_screen_name)
        return sm


if __name__ == '__main__':
    kwad.attach()
    ElectionsApp().run()
