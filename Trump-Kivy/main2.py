import kivy


kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader


class TrumpCard( Button ):
    myWavSound = SoundLoader.load('assets/stubs/Sounds/harp.wav')
    # shirt = ObjectProperty(None)
    # myWavSound = ObjectProperty(None)

    # def __init__(self, **kwargs):
    #
    #     Button.__init__(self, **kwargs)
    #     self.myWavSound = SoundLoader.load('assets/stubs/Sounds/harp.wav')

    def play_card(self):
        self.parent.scoreTrump += 1
        self.myWavSound.play()


class TrumpGame(FloatLayout):
    scoreTrump = NumericProperty(0)
    scoreHillary = NumericProperty(0)


class TrumpApp(App):
    def build(self):
        game = TrumpGame()
        return game

if __name__ == '__main__':
    TrumpApp().run()