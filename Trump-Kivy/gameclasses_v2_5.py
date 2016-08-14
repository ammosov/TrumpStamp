# collection of deck related functions and snippets

# ADD ASAP LOCALIZATION SUPPORT !!
# specifics - classes are strictly containers and pointers

import random
import csv

# VARIABLES

# PLACEHOLDER VARIABLES

# default players

trump = 0
hillary = 1

# default victory conditions

victory = {'destr': 999, 'res': 999}
winner = None
turn_counter = 0
players = []

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

path_t = ''  # path to images of Trump cards, default - same dir
path_h = ''  # path to images of Hillary cards, default - same dir

# FUNCTIONS


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
                # no error prevention is in place now !!
                # mb add later addl id_format='id' later
                for lbl in row:
                    a = row[lbl]
                    if is_int_str(a):  # convert numeric STR to INT
                        a = int(a)
                        newrow.update({lbl: a})
                    else:  # do not convert STR to STR
                        newrow.update({lbl: a})
            else:
                pass
        return newrow


def get_player_from_id(player_id):
    if player_id == 0:
        return trump
    elif player_id == 1:
        return hillary
    else:
        print 'Player id is not valid, must be 0 for Trump or 1 for Hillary'
        pass


def create_round(round_id):
    """take round.csv and create a round for a given round_id
    round includes creating two players, dealing cards and loading turn
    STANDS EMPTY !"""
    round_cond = get_row(round_db, round_id)  # get a line from CSV and convert to dictionary
    victory['destr'] = round_cond['destr']
    victory['res'] = round_cond['res']
    # set global variable victory to new conditions
    t_data, h_data = [0], [1]
    for i in range(1, 9):  # populates lists of initial Trump and Hillary parameters
        t_prefix = 't' + str(i)
        t_data.append(round_cond[t_prefix])
        h_prefix = 'h' + str(i)
        h_data.append(round_cond[h_prefix])
    trump = Player(t_data)
    hillary = Player(h_data)
    first_turn = round_cond['turn']
    if first_turn == 0:
        trump.set_active(1)
        hillary.set_active(0)
    elif first_turn == 1:
        trump.set_active(0)
        hillary.set_active(1)
    return trump, hillary


def sort_flatten_list(list1, list2):
    """https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions"""
    return sorted([num for elem in [list1, list2] for num in elem])


def create_decks(players, card_lists):
    """creates two initial decks and fills them with cards"""
    id_list = sort_flatten_list(card_lists[0], card_lists[1])
    trd = Deck()
    hld = Deck()
    # populate Decks with Cards and assign Card to Decks
    for i in id_list:
        # print Card(0, get_row(cards_db, i))
        card0 = Card(players[0], players[1], trd, get_row(cards_db, i))
        card0.set_deck(trd)
        trd.append(card0)
        card1 = Card(players[1], players[0], hld, get_row(cards_db, i))
        card1.set_deck(trd)
        hld.append(card1)
    return trd, hld


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
    def __init__(self, player_params):
        self.id = player_params[0]  # 0 = Trump, 1 = Hillary
        if self.id == 0:
            self.name = 'Trump'
        elif self.id == 1:
            self.name = 'Hillary'
        else:
            self.name = 'self.id not defined'
        self.swing = player_params[1]
        self.partisans = player_params[2]
        self.news = player_params[3]
        self.hype = player_params[4]
        self.cash = player_params[5]
        self.media = player_params[6]
        self.mojo = player_params[7]
        self.money = player_params[8]
        self.deck = 0  # pointer to Deck that Player owns
        self.hand = 0  # pointer to Hand that Player owns
        self.active = 0

    def __str__(self):
        return self.name

    def status(self):
        str1 = '{} has {} voters, of them {} swing voters and {} partisans, {} news, {} hype, {} cash, {} media, {} mojo, {} money.'
        str2 = ''
        if self.active == 0:
            str2 = '{} waits for turn'.format(self.name)
        elif self.active == 1:
            str2 = '{} makes next turn'.format(self.name)
        return str1.format(self.name, self.swing + self.partisans, self.swing, self.partisans, self.news, self.hype, self.cash,
                           self.media, self.mojo, self.money) + '\n' + str2

    def get_player_data(self, data_id):  # changes value according to type, needed to check card playablility
        if data_id == 0 or data_id == 'voters':
            return self.swing + self.partisans
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
        elif data_id == 9 or data_id == 'all resources':
            return [self.news, self.hype, self.cash]
        elif data_id == 10 or data_id == 'all assets':
            return [self.media, self.mojo, self.money]
        elif data_id == 11 or data_id == 'active':
            return self.active
        elif data_id == 12 or data_id == 'id':
            return self.id
        else:
            print 'invalid data_id, must be 0...11 or string param name'
            pass

    def get_player_id(self):  # fast player id retrieval
        return self.id

    def get_resources(self):  # fast check of card playability; zero added to account for free cards
        return [0, self.news, self.hype, self.cash]

    def card_action(self, value, action_type):  # card arguments modify player data per appropriate resource id, probably easiest way
        if action_type == 0:  # voters = swing + partisans, min value = 0; if damage greater than swing voters, only then partisans are damaged by the remainder
            self.partisans = max(0, self.partisans + self.swing + value)
            self.swing = max(0, self.swing + value)
        elif action_type == 1:  # swing voters, min = 0
            self.swing = max(0, self.swing + value)
        elif action_type == 2:  # partisans, min = 0
            self.partisans = max(0, self.partisans + value)
        elif action_type == 3:  # news, min = 0
            self.news = max(0, self.news + value)
        elif action_type == 4:  # hype, min = 0
            self.hype = max(0, self.hype + value)
        elif action_type == 5:  # cash, min = 0
            self.cash = max(0, self.cash + value)
        elif action_type == 6:  # media, min = 1
            self.media = max(1, self.media + value)
        elif action_type == 7:  # mojo, min = 1
            self.mojo = max(1, self.mojo + value)
        elif action_type == 8:  # money, min = 1
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

    def get_active(self):
        return self.active

    def reset(self):
        self.swing = 0
        self.partisans = 0
        self.news = 0
        self.hype = 0
        self.cash = 0
        self.media = 4
        self.mojo = 4
        self.money = 4


    def update_resources(self):  # at the end of turn, update resources of players
        self.news += self.media
        self.hype += self.mojo
        self.cash += self.money

class Card:
    """
    an object with n parameters
    for the time being Trump and Hillary use the same card values with different names
    """

    def __init__(self, player, opponent, deck, card_params):  # csv is processed outside card, card is fed params as a dict
        # print card_params
        self.player = player
        self.opponent = opponent
        self.card_id = card_params['id']
        self.description = card_params['descr']
        if self.player.get_player_id() == 0:
            self.name = card_params['ttitle'].replace('*', ' ')
            self.image = path_t + str(card_params['img_t'])
        elif self.player.get_player_id() == 1:
            self.name = card_params['htitle'].replace('*', ' ')
            self.image = path_h + str(card_params['img_t'])
        else:
            print 'error in card init, player id unrecognized'
        # check if card swallowed the player class
        # print 'player = {}, card id = {}'.format(self.player, self.card_id)
        self.cost_color = card_params['cost_color']
        self.cost_value = card_params['cost_value']
        self.action1 = [card_params['act1_value'], card_params['act1_type'], card_params['act1_side']]
        self.action2 = [card_params['act2_value'], card_params['act2_type'], card_params['act2_side']]
        self.action3 = [card_params['act3_value'], card_params['act3_type'], card_params['act3_side']]
        self.deck = deck  # Deck that Card belongs to
        self.playable = False  # Only Hand can declare a Card playable; True if player's resource equal or greater than cost
        self.inplay = False # Only Hand can declare a Card in play, one at a time

    def __repr__(self):
        return '{0} = {4}{1} ({2}/{3})'.format(self.card_id, self.name, self.cost_color, self.cost_value, '-!-' if self.playable else '')
        # return 'name = ' + str(self.name) + '\n color = ' + str(self.cost_color) + '\n cost = ' + str(self.cost_value) + '\n action3 = ' + str(self.action3)

    def play(self):
        self.player.set_active(0)
        self.opponent.set_active(1)
        if self.action1[2] == 0:
            self.player.card_action(self.action1[0], self.action1[1])
        elif self.action1[2] == 1:
            self.opponent.card_action(self.action1[0], self.action1[1])
        elif self.action1[2] == 2:
            self.player.card_action(self.action1[0], self.action1[1])
            self.opponent.card_action(self.action1[0], self.action1[1])

        if self.action2[2] == 0:
            if self.action2[2] == 11:
                self.player.set_active(1)
                self.opponent.set_active(0)
            else:
                self.player.card_action(self.action2[0], self.action2[1])
        elif self.action2[2] == 1:
            self.opponent.card_action(self.action2[0], self.action2[1])
        elif self.action2[2] == 2:
            self.player.card_action(self.action2[0], self.action2[1])
            self.opponent.card_action(self.action2[0], self.action2[1])

        if self.action3[2] == 0:
            if self.action3[2] == 11:
                self.player.set_active(1)
                self.opponent.set_active(0)
            else:
                self.player.card_action(self.action3[0], self.action3[1])
        elif self.action3[2] == 1:
            self.opponent.card_action(self.action3[0], self.action3[1])
        elif self.action3[2] == 2:
            self.player.card_action(self.action3[0], self.action3[1])
            self.opponent.card_action(self.action3[0], self.action3[1])
        else:
            print 'Side is not defined for action1, must be 0,1,2'

    def get_card_id(self):
        return self.card_id

    def get_name(self):
        return self.name

    def get_player(self):
        return self.player

    def get_opponent(self):
        return self.opponent

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

    def get_description(self):
        return self.description

    def set_deck(self, deck):
        self.deck = deck

    def get_deck(self):
        return self.deck

    def get_playable(self):
        return self.playable

    def set_playable(self, true_false):  # True or False kw only
        self.playable = true_false

    def set_inplay(self, true_false):
        self.inplay = true_false

class Deck:
    """Deck is a storage of Player-specific Cards, one Deck for each Player"""

    def __init__(self):
        self.cards = []
        self.player = 'not set'
        self.hand = 0  # Pointer to Hand to which Deck deals Cards

    def __str__(self):
        return 'Deck owner - {}'.format(str(self.player)) + '\n {}'.format('\n '.join(map(str, self.cards)))

    def set_hand(self, hand):
        self.hand = hand

    def set_player(self, player):
        self.player = player

    def deal(self, card):  # deal a card to Hand, assumes shuffled Deck; app. not used?
        self.hand.take_card(self.cards.pop(card))

    def shuffle(self):
        random.shuffle(self.cards)

    def pop_card(self):
        return self.cards.pop()

    def append(self, card):
        self.cards.append(card)

    def not_empty(self):
        if not self.cards:
            return False  # https://www.python.org/dev/peps/pep-0008/#id49
        else:
            return True

class Hand:
    def __init__(self, player_id):
        self.player_id = player_id
        self.player = get_player_from_id(self.player_id)
        self.deck = 0  # address to deck with a certain player id!
        # WAS self.cards = [Card(None, None), Card(None, None), Card(None, None), Card(None, None), Card(None, None), Card(None, None)]
        self.cards = [0, 0, 0, 0, 0, 0]

    def __repr__(self):
        # return '[%s]' % '\n '.join(map(str, self.cards))
        # return '\n '.join(map(str, self.cards))
        return 'Deck owner - {}'.format(str(self.player)) + '\n {}'.format('\n '.join(map(str, self.cards)))

    def set_player(self,player):
        self.player = player

    def take_card(self, card):
        for i in range(len(self.cards)):
            if 0 not in self.cards:
                print 'Hand full!'
            else:
                if self.cards[i] == 0:
                    self.cards[i] = card
                    break  # interrupts loop after the first occurence is found

    def deal_card(self, card):
        for i in range(6):
            if self.cards[i] == 0:
                card.set_playable(True)
                self.cards[i] = card
            else:
                pass

    def set_playables(self):  # resets playability at the end of player's turn, assumes 6 cards !!
        res = self.player.get_resources()  # how do i find the necessary player object?
        for card in self.cards:
            color = card.get_cost_color()
            value = card.get_cost_value()
            if color == 0 and value == 99:
                if res[1] >= 99 and res[2] >= 99 and res[3] >= 99:
                    card.set_playable(True)
                else:
                    card.set_playable(False)
            elif res[color] >= value:
                card.set_playable(True)
            else:
                card.set_playable(False)

    def get_playable_cards(self):  # returns a list of playable cards; can be empty!
        playable_cards = []
        for n in self.cards:
            if n.get_playable():
                playable_cards.append(n)
        if not playable_cards:  # required method to check if list is empty
            # print 'No playable cards in this deck!'
            pass
        return playable_cards

    def list_playable(self):  # returns a list of 6 playabilities! will be used to screen cards on the field
        playable = []
        for n in self.cards:
            if n == 0:
                playable.append(False)
            else:
                playable.append(n.get_playable())
        return playable

    def play_card(self, card_index):  # card_index is 0-5 index of card in deck
        card = self.cards[card_index]
        if card.get_playable():
            card.set_inplay(True)
            self.cards.pop(card)
        # active_card becomes card




            # TESTS MOVED TO EXTERNAL FILE