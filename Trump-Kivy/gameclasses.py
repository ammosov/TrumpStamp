# collection of deck related functions and snippets

# ADD ASAP LOCALIZATION SUPPORT !!

import random
import csv

# types, sides label-value pairs

types = {
    0: "Voters",
    1: "Swing Voters",
    2: "Partisans",
    3: "News",
    4: "Hype",
    5: "Cash",
    6: "Media",
    7: "Mojo",
    8: "Money",
    9: "all resources",
    10: "all assets",
    11: "Free turn"
}
sides = {
    0: "to you",
    1: "to opp",
    2: "to both"
}

# default victory conditions

victory = {'destr': 1, 'res': 999}

# EXTERNAL DATABASES CONNECTED

round_db = "rounds.csv"
# csv with current round parameters -
# victory conditions, first turn, player parameters at start

cards_db = "cards.csv"
# csv with card values
# format - ID, title_t, title_h,
# cost_color, cost_value, descr,
# act1_value, act1_type, act1_side,
# act2_value_value, act2_type, act2_side,
# act3_value, act3_type, act3_side,
# img_t, img_h

# FUNCTIONS

path_t = '' # path to images of Trump cards, default - same dir
path_h = '' # path to images of Hillary cards, default - same dir

def index_to_type(index):
    """shorthand for getting a type name from index"""
    return types[index]


def type_to_index(sometype):
    """get an index of a given type name"""
    reverse_types = {v: k for k, v in types.items()}
    return reverse_types[sometype]


def is_int_str(v):
    """
    sort of complex expression to check for numeric values that come for csv as strings
    see http://stackoverflow.com/questions/1265665/python-check-if-a-string-represents-an-int-without-using-try-except
    """
    v = str(v).strip()
    return v == '0' or (v if v.find('..') > -1 else v.lstrip('-+').rstrip('0').rstrip('.')).isdigit()


def get_row(csvfile, row_id):
    """input: csv file, id of a line;
    id must be labeled as 'id' - or else!
    output: dictionary with headers as keys and row values as values"""
    with open(csvfile, 'rb') as csvfile:
        newfile = csv.DictReader(csvfile, delimiter=',', quotechar='|')
        newrow = {}  # empty dictionary
        for row in newfile:
            if row['id'] == str(row_id):
                # id is numeric but at this point as it comes out of CSV, it is still a string!
                # row['id'] -> 'id' must be present in CSV or else!
                # mb add later addl id_format='id' later
                for lbl in row:
                    a = row[lbl]
                    if is_int_str(a):  # convert numeric STR to INT
                        a = int(a)
                        newrow.update({lbl: a})
                    else:  # do not convert STR to STR
                        newrow.update({lbl: a})
        return newrow


def create_round(round_id):
    """take round.csv and create a round for a given round_id
    round includes creating two players, dealing cards and loading turn
    STANDS EMPTY !"""
    round_cond = get_row(round_db, round_id)  # get a line from CSV and convert to dictionary
    victory['destr'] = round_cond['destr']
    victory['res'] = round_cond['res']
    # set global variable victory to new conditions
    t = []  # Trump characteristics
    h = []  # Hillary characteristics
    first_turn = round_cond['turn']
    if first_turn == 0:
        t.append(1)
        h.append(0)
    elif first_turn == 1:
        t.append(0)
        h.append(1)
    else:
        print 'first turn not defined!'
    for i in range(1, 9):
        t_prefix = 't' + str(i)
        t.append(round_cond[t_prefix])
        h_prefix = 'h' + str(i)
        h.append(round_cond[h_prefix])
    # print statements - replace with code to create players
    trump = Player(0, t)
    hillary = Player(1, h)
    return trump, hillary


# CLASSES


class Player:
    """
    initiated with id = 0/1 and player_data = (0-7)
    player_data sequence: Swing Voters, Partisans, News, Hype, Cash, Media, Mojo, Money
    in ROUNDS.CSV, voters param in database is replaced by first turn ID - 1 starts the game
    this is currently a player data container
    created with a create_round function only!
    """

    # def __init__(self, player_id, swing, partisans, news, hype, cash, media, mojo, money):
    def __init__(self, player_id, player_params):
        self.id = player_id
        if self.id == 0:
            self.name = 'Trump'
        elif self.id == 1:
            self.name = 'Hillary'
        else:
            self.name = 'self.id not defined'
        self.active = player_params[0]  # 0 = player cannot play cards, 1 = can play
        self.swing = player_params[1]
        self.partisans = player_params[2]
        self.news = player_params[3]
        self.hype = player_params[4]
        self.cash = player_params[5]
        self.media = player_params[6]
        self.mojo = player_params[7]
        self.money = player_params[8]
        self.voters = self.swing + self.partisans

    def __str__(self):
        return self.name

    def status(self):
        str1 = '{} has {} voters, of them {} swing voters and {} partisans, {} news, {} hype, {} cash, {} media, {} mojo, {} money.'
        str2 = ''
        if self.active == 0:
            str2 = '{} waits for turn'.format(self.name)
        elif self.active == 1:
            str2 = '{} makes next turn'.format(self.name)
        return str1.format(self.name, self.voters, self.swing, self.partisans, self.news, self.hype, self.cash,
                           self.media, self.mojo, self.money) + '\n' + str2

    def get_player_data(self, data_id):  # returns value according to type, needed to check card playablility
        if data_id == 0 or data_id == 'voters':
            return self.voters
        elif data_id == 1 or data_id == 'swing':
            return self.swing
        elif data_id == 2 or data_id == 'partisans':
            return self.partisans
        elif data_id == 3 or data_id == 'news':
            return self.news
        elif data_id == 4 or data_id == 'hype':
            return self.hype
        elif data_id == 5 or data_id == 'cash':
            return self.cash
        elif data_id == 6 or data_id == 'media':
            return self.media
        elif data_id == 7 or data_id == 'mojo':
            return self.mojo
        elif data_id == 8 or data_id == 'money':
            return self.money
        elif data_id == 11 or data_id == 'active':
            return self.active
        else:
            print 'invalid data_id, must be 0...8..11 or string param name'
            pass

    def card_playable(self, cost_color,
                      cost_value):  # alternative way to check if player has enough resources for a given card, returns True if card is playable
        if cost_color == 1:
            return self.news > cost_value
        elif cost_color == 2:
            return self.hype > cost_value
        elif cost_color == 3:
            return self.cash > cost_value
        else:
            print 'invalid cost_color, must be 1...3'

    def card_action(self, value, action_type):  # card arguments modify player data per appropriate resource id
        if action_type == 0:  # voters = swing + partisans, if damage greater than swing voters, only then partisans are damaged by the remainder
            self.partisans += min(0, self.swing + value)
            self.swing = max(0, self.swing + value)
            self.voters = self.swing + self.partisans
        elif action_type == 1:  # swing voters
            self.swing = max(0, self.swing + value)
            self.voters = self.swing + self.partisans
        elif action_type == 2:  # partisans
            self.partisans = max(0, self.partisans + value)
            self.voters = self.swing + self.partisans
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
        elif action_type == 11:  # new turn, nothing is changed
            self.active = 1
        else:
            print 'invalid action type, must be 0...11'
            pass

    def set_active(self, code):
        self.active = code


class Card:
    """
    an object with n parameters
    for the time being Trump and Hillary use the same card values with different names

    """

    def __init__(self, player_id, card_params):  # csv is processed outside card, card is fed params as a dict
        self.player_id = player_id
        self.card_id = card_params['id']
        if self.player_id == 0:
            self.name = card_params['ttitle']
            self.image = path_t + str(card_params['img_t'])
        elif self.player_id == 1:
            self.name = card_params['htitle']
            self.image = path_h + str(card_params['img_t'])
        self.cost_color = card_params['cost_color']
        self.cost_value = card_params['cost_value']
        self.action1 = [card_params['act1_value'], card_params['act1_type'], card_params['act1_side']]
        self.action2 = [card_params['act2_value'], card_params['act2_type'], card_params['act2_side']]
        self.action3 = [card_params['act3_value'], card_params['act3_type'], card_params['act3_side']]
        self.playable = 0

    def __str__(self):
        return 'name = ' + str(self.name) + '\n color = ' + str(self.cost_color) + '\n cost = ' + str(self.cost_value) + '\n action3 = ' + str(self.action3)

    def get_card_id(self):
        return self.card_id

    def get_name(self):
        return self.name

    def get_player_id(self):
        return self.player_id

    def get_cost_color(self):
        return self.cost_color

    def get_cost_value(self):
        return self.cost_value

    def get_actions(self, action_id):
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

'''
class Deck:
    """docstring"""

    def __init__(self, player_id):
        self.cards = []
        self.player_id = player_id
        for i in cards_db:
            if i == player_id:  # check a player ID
                # get card parameters
                self.cards.append(Card(player))  # generate a card with these parameters and add to deck
            else:
                pass
        pass

    def __str__(self):
        return self.cards

    def deal(self):  # deal a card
        pass

    def shuffle(self):
        random.shuffle(self)

    def pop_card(self):
        return self.card.pop

    def append_card(self, card):
        self.cards.append(card)


class Hand(Deck):
    def __init__(self, player_id):
        Deck.__init__(self, player_id)
        self.cards = []
        self.player_id = player_id

'''

# TESTS MOVED TO EXTERNAL FILE