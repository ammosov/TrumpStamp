from kivy.properties import BoundedNumericProperty, ListProperty
from kivy.uix.widget import Widget
from deck import Deck
from hand import Hand

PLAYERS = {0: 'Trump',
           1: 'Hillary'}


class Player(Widget):
    partisans = BoundedNumericProperty(0, min=0, max=125, rebind=True)
    swing_voters = BoundedNumericProperty(0, min=0)
    media = BoundedNumericProperty(1, min=1, max=100)
    news = BoundedNumericProperty(1, min=0, max=300)
    mojo = BoundedNumericProperty(1, min=1, max=100)
    hype = BoundedNumericProperty(1, min=0, max=300)
    money = BoundedNumericProperty(1, min=1, max=100)
    cash = BoundedNumericProperty(1, min=0, max=300)

    cards_actions = ListProperty([])

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.player_id = None
        self.player_name = None
        self.stats = None

    def late_init(self, **kwargs):
        self.player_id = kwargs.pop('player_id')
        self.card_fabric = kwargs.pop('card_fabric')
        self.player_name = PLAYERS[self.player_id]
        self.stats = kwargs
        for prop_name, value in self.stats.items():
            setattr(self, prop_name, value)

        self.RESOURSES = {1: self.news, 2: self.cash, 3: self.hype}

        self.active = False  # Active Player plays the next Card
        self.human = False  # Human player == True gets HID input, False = algorithm plays
        self.winner = None

        self.deck = Deck(self, self.card_fabric)
        self.hand = Hand(self, self.deck)

    def set_opponent(self, opponent):
        """Sets opponents at once for Player and all his objects"""
        self.opponent = opponent
        #self.deck.set_opponent(self.opponent)
        #self.hand.set_opponent(self.opponent)

    def set_active(self, active):
        self.active = active

    def get_active(self):
        return self.active

    def get_deck(self):
        return self.deck
    
    def get_hand(self):
        return self.hand

    def get_player_id(self):
        return self.player_id

    def pay_for_card(self, card_color, card_value):
        if card_color:
            if (self.RESOURSES[card_color] - card_value) >= 0 :
                self.RESOURSES[card_color] -= card_value
            else:
                return false
        else:
            for res in self.RESOURSES.values():
                if (res - card_value) >= 0:
                    res -= card_value
                else:
                    return false
        return true
        





