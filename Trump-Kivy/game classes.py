# collection of deck related functions and snippets

import random

"""
ADD ASAP LOCALIZATION SUPPORT !!
"""

types = {
0:'Voters',
1:'Swing Voters',
2:'Partisans',
3:'News',
4:'Hype',
5:'Cash',
6:'Media',
7:'Mojo',
8:'Money',
9:'all resources',
10:'all assets',
11:'Free turn'
}
sides = {0:'to you', 1:'to opp', 2:'to both'}

cards_db = "cards.xml"

class Player:
    """
    initiated with id = 0/1 and player_data = (0-7)
    player_data sequence: Swing Voters, Partisans, News, Hype, Cash, Media, Mojo, Money'
    this is currently a player data container
    """

    def __init__(self, player_id, swing, partisans, news, hype, cash, media, mojo, money):
        self.id = player_id
        if self.id == 0:
            self.name = 'Hillary'
        elif self.id == 1:
            self.name = 'Trump'
        else:
            self.name = 'self.id not defined'
        self.voters = swing + partisans
        self.swing = swing
        self.partisans = partisans
        self.news = news
        self.hype = hype
        self.cash = cash
        self.media = media
        self.mojo = mojo
        self.money = money
        self.active = 0 #  0 = player cannot play cards, 1 = can play

    def __str__(self):
        return self.name

    def status(self):
        str1 = '{} has {} voters, of them {} swing voters and {} partisans, {} news, {} hype, {} cash, {} media, {} mojo, {} money.'
        return str1.format(self.name, self.voters, self.swing, self.partisans, self.news, self.hype, self.cash, self.media, self.mojo, self.money)

    def get_player_data(self,data_id):  # returns value according to type, needed to check card playablility
        if data_id == 0:
            return self.voters
        elif data_id == 1:
            return self.swing
        elif data_id == 2:
            return self.partisans
        elif data_id == 3:
            return self.news
        elif data_id == 4:
            return self.hype
        elif data_id == 5:
            return self.cash
        elif data_id == 6:
            return self.media
        elif data_id == 7:
            return self.mojo
        elif data_id == 8:
            return self.money
        else:
            print 'invalid data_id, must be 0...8'
            pass

    def card_playable(self,cost_color, cost_value):  # alternative way to check if player has enough resources for a given card, returns True if card is playable
        if cost_color == 1:
            return self.news > cost_value
        elif cost_color == 2:
            return self.hype > cost_value
        elif cost_color == 3:
            return self.cash > cost_value
        else:
            print 'invalid cost_color, must be 1...3'

    def card_action(self,value,action_type):  # card arguments modify player data per appropriate resource id
        if action_type == 0: # voters = swing + partisans, if damage greater than swing voters, only then partisans are damaged by the remainder
            self.partisans += min(0,self.swing + value)
            self.swing = max(0, self.swing + value)
        elif action_type == 1:  # swing voters
            self.swing = max(0,self.swing + value)
        elif action_type == 2:  # partisans
            self.partisans = max(0,self.partisans + value)
        elif action_type == 3:  # news
            self.news = max(0, self.news + value)
        elif action_type == 4:  # hype
            self.hype = max(0, self.hype + value)
        elif action_type == 5:  # cash
            self.cash = max(0, self.cash + value)
        elif action_type == 6:  # media
            self.media = max(1, self.media + value)
        elif action_type == 7:  # mojo
            self.mojo = max(1, self.mojo + value)
        elif action_type == 8:  # money
            self.money = max(1, self.money + value)
        elif action_type == 9:  # all resources
            self.news = max(0, self.news + value)
            self.hype = max(0, self.hype + value)
            self.cash = max(0, self.cash + value)
        elif action_type == 10:  # all assets
            self.media = max(1, self.media + value)
            self.mojo = max(1, self.mojo + value)
            self.money = max(1, self.money + value)
        elif action_type == 11: # new turn, nothing is changed
            self.active = 1
        else:
            print 'invalid action type, must be 0...11'
            pass

    def set_active(self,code):
        self.active = code



class Card:
    """
    an object with n parameters
    for the time being Trump and Hillary use the same card values with different names
    """

    def __init__(self, name, player, cost_value, cost_color, action1, action2=None, action3=None, image):  # action1-3 are tuple of 3 elements
        self.name = name
        self.player = player
        self.cost_value = cost_value
        self.cost_color = cost_color
        self.action1 = action1
        self.action2 = action2
        self.action3 = action3
        self.image = image
        self.playable = 0

    def __str__(self):
        return str(self.name)

    def get_name(self):
        return self.name
    def get_player(self):
        return self.player
    def get_cost_color(self):
        return self.cost_color
    def get_cost_value(self):
        return self.cost_value
    def get_actions(self,action_id):
        if action_id == 1:
            return self.action1
        elif action_id == 2:
            return self.action2
        elif action_id == 3:
            return self.action3
        else:
            print 'action_id invalid, must be 1...3'
            pass
    def get_image(self):
        return self.image
    def get_playable(self):
        return self.playable

class Deck:
    """docstring"""

    def __init__(self, player_id):
        self.cards = []
        for i in cards_db:
            if i == player_id: #  check a player ID
                # get card parameters
                self.cards.append(Card(player)) #  generate a card with these parameters and add to deck
            else:
                pass
        pass

    def __str__(self):
        pass

    def deal(self): # deal a card
        pass

    def shuffle(self):
        random.shuffle(self)

    def pop_card(self):
        return self.card.pop

    def append_card(self,card):
        self.cards.append(self,card)


class Hand (Deck):

    def __init__(self):
        pass

    def __str__(self):
        pass

