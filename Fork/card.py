from kivy.core.audio import SoundLoader
from kivy.properties import BoundedNumericProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.logger import Logger


class Card(Button, Widget):
    sound = SoundLoader.load('assets/stubs/Sounds/card.wav')
    background_normal = 'assets/card00.png'

    def __init__(self, *args, **kwargs):
        super(Card, self).__init__(*args, **kwargs)


    def play_card(self):
        self.sound.play()
