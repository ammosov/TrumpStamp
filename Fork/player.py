from kivy.properties import BoundedNumericProperty, ListProperty
from kivy.uix.widget import Widget
from deck import Deck
from hand import Hand

PLAYERS = {0: 'PlayerTrump',
           1: 'PlayerHillary'}


class Player(Widget):
    partisans = BoundedNumericProperty(0, min=0, max=125, rebind=True)
    swing = BoundedNumericProperty(0, min=0)
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
            print prop_name, value
            self.property(prop_name).set(self, value)

        self.RESOURSES = {1: 'news', 2: 'cash', 3: 'hype'}
        self.ACTIONS = {1: ['swing'], 2: ['partisans'], 3: ['news'], 4: ['hype'], 5: ['cash'],
                        6: ['media'], 7: ['mojo'], 8: ['money'], 9:  ['news', 'hype', 'cash'], 
                        10: ['media', 'mojo', 'money']}
        self.active = False  # Active Player plays the next Card
        self.human = False  # Human player == True gets HID input, False = algorithm plays
        self.winner = None

        self.deck = Deck(self, self.card_fabric)
        self.hand = Hand(self.deck)

    def set_opponent(self, opponent):
        """Sets opponents at once for Player and all his objects"""
        self.opponent = opponent
        #self.deck.set_opponent(self.opponent)
        #self.hand.set_opponent(self.opponent)

    def set_active(self, active):
        self.active = active
        # TODO
        # bot should do turn here
        # innleg_play ():
        #       self.opponent_swing
                #self.hand.get_cards()
                #card = Analysis
                #card.on_press()


    def get_active(self):
        return self.active

    def set_winner(self, winner):
        self.winner = winner

    def get_deck(self):
        return self.deck
    
    def get_hand(self):
        return self.hand

    def get_player_id(self):
        return self.player_id

    def get_voters(self):
        return self.partisans

    def pay_for_card(self, card_color, card_value):
        if card_color:
            property = self.property(self.RESOURSES[card_color])
            property_value = property.get(self)
            if (property_value - card_value) >= 0 :
                property.set(self, property_value - card_value)
            else:
                return False
        else:
            for color, prop_name in self.RESOURSES.items():
                property = self.property(prop_name)
                property_value = property.get(self)
                if (property_value - card_value) >= 0:
                    property.set(self, property_value - card_value)
                else:
                    return False
        return True

    def apply_card(self, type, value):
        if type == 0:
            if value > 0:
                self.swing += value
            # lose voters branch
            elif value < 0:
                self.partisans = max(0, self.partisans + self.swing + value)
                self.swing = max(0, self.swing + value)
            else:
                pass
        elif type == 11:
            pass
        else:
            for res in self.ACTIONS[type]:
                #TODO
                # check with -value, it's seem it doesn't work(( 
                old_value = self.property(res).get(self)
                min_value = self.property(res).get_min(self)
                #print self.player_id, res, type, value, old_value, min_value
                self.property(res).set(self, max(min_value, old_value + value))

    def update_resources(self):  # at the end of turn, update resources of players
        for fabric, resource in (('media', 'news'), ('mojo', 'hype'), ('money', 'cash')):
            fabric_property = self.property(fabric)
            fabric_property_value = fabric_property.get(self)
            resource_property = self.property(resource)
            resource_property_value = resource_property.get(self)
            resource_property.set(self, fabric_property_value + resource_property_value)
