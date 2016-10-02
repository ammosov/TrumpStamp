"""Main module."""
import kivy
import kwad
from kivy.app import App
from kivy.config import Config
from kivy.uix.screenmanager import ScreenManager
import start_screen
import end_screen


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
        start_screen_ = start_screen.StartScreen(sm, name=self.start_screen_name)
        sm.switch_to(start_screen_)
        return sm

    def on_pause(self):
        """Handle suspend on android."""
        return True

if __name__ == '__main__':
    kwad.attach()
    ElectionsApp().run()
