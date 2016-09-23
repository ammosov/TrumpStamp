from kivy.animation import Animation
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget

from kivy.properties import BoundedNumericProperty, ObjectProperty


class Card(Button, Widget):
    """ card_id is an id from cards.csv, number_in_hand in [0, 5]"""
    def __init__(self, card_id, card_holder, number_in_hand):
        Widget.__init__(self)
        Button.__init__(self)
        self.card_id = card_id
        self.card_holder = card_holder
        self.number_in_hand = number_in_hand
        self.background_normal = 'assets/cards/' + str(card_holder) + '/1' + str(card_id)

    def on_touch_up(self, touch):
        if self.card_holder.is_active:
            self.card_holder.play_card(self.card_id, self.number_in_hand)

    def on_touch_down(self, touch):
        if self.card_holder.is_active:
            self.card_holder.discard(self.card_id, self.number_in_hand)
            animation = Animation(x=50, size=(80, 80), t='in_quad')
            animation.start(self)


class Hand(Widget):
    pass


class Player(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.hand = Hand()
        self.is_active = False

    partisans = BoundedNumericProperty(0, min=0, max=125, rebind=True)
    swing_voters = BoundedNumericProperty(0, min=0)

    media = BoundedNumericProperty(1, min=1, max=100)
    news = BoundedNumericProperty(1, min=0, max=300)
    mojo = BoundedNumericProperty(1, min=1, max=100)
    charisma = BoundedNumericProperty(1, min=0, max=300)
    donors = BoundedNumericProperty(1, min=1, max=100)
    cash = BoundedNumericProperty(1, min=0, max=300)

    def play_card(self, card_id, number_in_hand):
        pass

    def discard_card(self, card_id, number_in_hand):
        pass


class Deck:
    def __init__(self):
        pass
        # cards = [] load cards


class ElectionsGame(Widget):
    deck = ObjectProperty(None)
    playerTrump = ObjectProperty(Player)
    playerHillary = ObjectProperty(Player)

    def deal_deck(self):
        pass

    def set_active_player(self, player_name):
        if player_name == 'Trump':
            self.playerTrump.is_active = True
        else:
            self.playerHillary.is_active = True


class ElectionsApp(App):
    def build(self):
        game = ElectionsGame()
        game.deal_deck()
        # Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game


if __name__ == '__main__':
    ElectionsApp().run()
