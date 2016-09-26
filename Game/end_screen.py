from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.button import Button

class EndScreen(Screen):

    def __init__(self, sm, **kwargs):
        super(EndScreen, self).__init__(**kwargs)
