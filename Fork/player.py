from kivy.properties import BoundedNumericProperty, ListProperty
from kivy.uix.widget import Widget

PLAYERS = {0: 'Trump',
           1: 'Hillary'}


class Player(Widget):
    partisans = BoundedNumericProperty(0, min=0, max=125, rebind=True)
    swing_voters = BoundedNumericProperty(0, min=0)
    media = BoundedNumericProperty(1, min=1, max=100)
    news = BoundedNumericProperty(1, min=0, max=300)
    mojo = BoundedNumericProperty(1, min=1, max=100)
    charisma = BoundedNumericProperty(1, min=0, max=300)
    donors = BoundedNumericProperty(1, min=1, max=100)
    cash = BoundedNumericProperty(1, min=0, max=300)

    # noinspection PyArgumentList
    cards_actions = ListProperty([])

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.player_id = None
        self.player_name = None
        self.stats = None

    def late_init(self, **kwargs):
        self.player_id = kwargs.pop('player_id')
        self.player_name = PLAYERS[self.player_id]
        self.stats = kwargs
        for prop_name, value in self.stats.items():
            setattr(self, prop_name, value)
