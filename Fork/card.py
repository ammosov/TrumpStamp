from kivy.core.audio import SoundLoader
from kivy.properties import BoundedNumericProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.logger import Logger
import pandas as pd
import os


class Card(Button, Widget):
    sound = SoundLoader.load('assets/stubs/Sounds/card.wav')
    background_normal = 'assets/card00.png'

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)


    def lazy_init(self, **kwargs):

        pass

    def play_card(self):
        self.sound.play()


class Cards(object):
    def __init__(self, card_db):
        self.db = pd.read_csv(card_db)

    def get_card(self, card_id):
        return Card()


if __name__ == '__main__':
    SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
    cards = Cards(os.path.join(SCRIPT_DIR, 'cards.csv'))
    print cards.get_card(1)