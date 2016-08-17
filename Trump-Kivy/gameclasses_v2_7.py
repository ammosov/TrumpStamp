# collection of deck related functions and snippets

# ADD ASAP LOCALIZATION SUPPORT !!
# specifics - classes are strictly containers and pointers

import random
import csv

# VARIABLES

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
# they mostly do technical things and procedures


def is_int_str(v):
    """
    sort of complex expression to check for numeric values that come from csv as strings
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


def sort_flatten_list(list1, list2):
    """Flattens and sorts list of cards before generation
    https://docs.python.org/3/tutorial/datastructures.html#list-comprehensions"""
    return sorted([num for elem in [list1, list2] for num in elem])

# CLASSES

class GameMaster:
    """CONTAINER FOR GAME VARIABLES, PROCESSES AND FUNCTIONS
    """

    def __init__(self, round_id):
        """CREATES ALL GAME TERMS, PLAYERS, DECKS, HANDS AND CARDS AT ONCE"""
        # START GAME
        self.game_over = False
        self.winner = None
        # GAME TERMS
        # get a line of round conditions from CSV, converted to dictionary
        round_cond = get_row(round_db, round_id)
        # select allowed cards by id
        # NOTE !! TEMP !! this is not a good way to do it, should be different and set in config
        self.cards = [range(1, 53)]  # list of cards in sequence
        self.additional_cards = [99]  # list of non sequential cards
        id_list = sort_flatten_list(self.cards[0], self.additional_cards)  # makes a list of card ids
        # set victory variables to new conditions
        # so far it's just two of them
        # destr: 0 == all voters must reach 0
        # res: 0-999 == any of resources must reach this value
        self.victory = {'destr': round_cond['destr'], 'res': round_cond['res']}
        # CREATE PLAYERS
        # populates lists of initial Trump and Hillary parameters
        t_data, h_data = [0], [1]  # these numbers are for consistency, see Player__init__ notes
        # parameters are labeled as t0-t1, digit points to resource code per card database
        # round_cond reads them, then they are added to list and passed to Player() when done
        for i in range(1, 9):
            t_prefix = 't' + str(i)
            t_data.append(round_cond[t_prefix])
            h_prefix = 'h' + str(i)
            h_data.append(round_cond[h_prefix])
        self.trump = Player(t_data)
        self.hillary = Player(h_data)
        # set both players to active and passive state based on who starts
        if round_cond['turn'] == 0:
            self.trump.set_active(True)
            self.hillary.set_active(False)
        elif round_cond['turn'] == 1:
            self.trump.set_active(False)
            self.hillary.set_active(True)
        else:
            print 'GameMater INIT: ERROR ! First turn is not set!'
        # CREATE DECKS
        # creates two initial Decks
        self.trump_deck = Deck()
        self.hillary_deck = Deck()
        # CREATE HANDS
        # generate two initial Hands
        self.trump_hand = Hand()
        self.hillary_hand = Hand()
        # SET CONNECTIONS BTW PLAYERS, DECKS AND HANDS
        # assign to Players Hands and Decks
        self.trump.set_deck(self.trump_deck)
        self.trump.set_hand(self.trump_hand)
        self.hillary.set_deck(self.hillary_deck)
        self.hillary.set_hand(self.hillary_hand)
        # assign to Decks Players and Hands
        self.trump_deck.set_player(self.trump)
        self.trump_deck.set_hand(self.trump_hand)
        self.hillary_deck.set_player(self.hillary)
        self.hillary_deck.set_hand(self.trump_hand)
        # assign  to Hands Players and Decks
        self.trump_hand.set_player(self.trump)
        self.trump_hand.set_deck(self.trump_deck)
        self.hillary_hand.set_player(self.hillary)
        self.hillary_hand.set_deck(self.hillary_deck)
        # CREATE CARDS
        # populate Decks with Cards and assign Card to Decks
        # database contains identical cards for Trump anf Hillary
        # every card is therefore created twice, for each of players
        for i in id_list:
            card0 = Card(self.trump, self.hillary, self.trump_deck, get_row(cards_db, i))
            self.trump_deck.append(card0)
            card1 = Card(self.hillary, self.trump, self.hillary_deck, get_row(cards_db, i))
            self.hillary_deck.append(card1)
        # shuffle Decks
        self.trump_deck.shuffle()
        self.hillary_deck.shuffle()
        # deal 6 Cards from Decks to Hands
        self.trump_hand.refill()
        self.hillary_hand.refill()
        self.trump_hand.set_playables()
        self.hillary_hand.set_playables()
        # the game is ready to play

    def __repr__(self):
        # should print smth about the game. will decide later.
        return 'Active = {} - {}\n\n{} - {}'.format(self.trump.get_active(), self.trump_hand, self.hillary.get_active(), self.hillary_hand)

    def get_active_player(self):
        # probably can be rid of
        if self.trump.get_active() and not self.hillary.get_active():
            return self.trump
        elif not self.trump.get_active() and self.hillary.get_active():
            return self.hillary
        else:
            print 'GameMaster.get_active_player says: ' \
                  'Trump active = {} ; Hillary active = {}'.format(self.trump.get_active(), self.hillary.get_active())

    def switch_active_players(self):
        """changes active status to passive and back
        !! check for correct not notation! """
        # case 1 - make Trump active
        if not self.trump.get_active() and self.hillary.get_active():
            self.trump.set_active(True)
            self.hillary.set_active(False)
        # case 2 - make Hillary active
        elif self.trump.get_active() and not self.hillary.get_active():
            self.trump.set_active(False)
            self.hillary.set_active(True)
        else:
            print 'GameMaster.switch_active_players says: ERROR!'

    def declare_victory(self):
        """checks if victory is achieved"""
        # if Trump wins
        if (self.trump.get_player_data('voters') == self.victory['destr']
            or self.trump.get_player_data('news') == self.victory['res']
            or self.trump.get_player_data('hype') == self.victory['res']
            or self.trump.get_player_data('cash') == self.victory['res']
            ):
            self.trump.set_winner(True)
            self.game_over = True
            return True
        # if Hillary wins
        elif (self.hillary.get_player_data('voters') == self.victory['destr']
              or self.hillary.get_player_data('news') == self.victory['res']
              or self.hillary.get_player_data('hype') == self.victory['res']
              or self.hillary.get_player_data('cash') == self.victory['res']
              ):
            self.hillary.set_winner(True)
            self.game_over = True
            return True
        # No winner yet
        else:
            return False

    def turn_if_switch(self):
        if self.declare_victory():
            pass
        # Keep in mind - every card after play
        # sets itself its owner's player_active to False
        # unless it's a free turn card
        elif self.trump.get_active():
            while self.trump.get_active():
                if not self.trump_hand.get_playable_cards():
                    print ' GM.switch turn branch 1'
                    self.switch_active_players()
                    # break
                self.trump_hand.play_random_card()  # assumes Trump is not human - random playable card
                # self.trump_hand.play_selected_card(raw_input())  # assumes Trump is human - HID actions to select a card
                if self.declare_victory():
                    break
            while self.hillary.get_active():
                if not self.hillary_hand.get_playable_cards():
                    print ' GM.switch turn branch 2'
                    self.switch_active_players()
                    # break
                self.hillary_hand.play_random_card()  # assumes Hillary is not human - random playable card
                if self.declare_victory():
                    break
        elif self.hillary.get_active():
            while self.hillary.get_active():
                if not self.hillary_hand.get_playable_cards():
                    print ' GM.switch turn branch 3'
                    self.switch_active_players()
                    # break
                self.hillary_hand.play_random_card()  # assumes Hillary is not human - random playable card
                if self.declare_victory():
                    break
            while self.trump.get_active():
                if not self.trump_hand.get_playable_cards():
                    print ' GM.switch turn branch 4'
                    self.switch_active_players()
                    # break
                self.trump_hand.play_random_card()  # assumes Trump is not human - random playable card
                # self.trump_hand.play_selected_card(raw_input())  # assumes Trump is human - HID actions to select a card
                if self.declare_victory():
                    break
        else:
            print 'GameMaster.turn says: ' \
                  'Trump active = {} ; Hillary active = {}'.format(self.trump.get_active(), self.hillary.get_active())
        self.trump.update_resources()
        self.hillary.update_resources()
        self.trump_hand.refill()
        self.hillary_hand.refill()
        print '{}'.format(self.trump.status())
        print '{}'.format(self.hillary.status())

    def turn_if_discard(self):
        if self.declare_victory():
            pass
        # Keep in mind - every card after play
        # sets itself its owner's player_active to False
        # unless it's a free turn card
        elif self.trump.get_active():
            while self.trump.get_active():
                self.trump_hand.play_discard_random_card()  # assumes Trump is not human - random playable card
                if self.declare_victory():
                    break
            while self.hillary.get_active():
                self.hillary_hand.play_discard_random_card()  # assumes Hillary is not human - random playable card
                if self.declare_victory():
                    break
        elif self.hillary.get_active():
            while self.hillary.get_active():
                self.hillary_hand.play_discard_random_card()  # assumes Hillary is not human - random playable card
                if self.declare_victory():
                    break
            while self.trump.get_active():
                self.trump_hand.play_discard_random_card()  # assumes Trump is not human - random playable card
                if self.declare_victory():
                    break
        else:
            print 'GameMaster.turn says: ' \
                  'Trump active = {} ; Hillary active = {}'.format(self.trump.get_active(), self.hillary.get_active())
        self.trump.update_resources()
        self.hillary.update_resources()
        print 'Res upd'
        self.trump_hand.refill()
        self.hillary_hand.refill()
        self.trump_hand.set_playables()
        self.hillary_hand.set_playables()
        print 'Crd dlt'
        print '{}'.format(self.trump.status())
        print '{}'.format(self.hillary.status())


class Player:
    """CONTAINER FOR PLAYER PARAMETERS
    initiated with id = 0/1 and player_data = (0-7)
    player_data sequence: Swing Voters, Partisans, News, Hype, Cash, Media, Mojo, Money
    in ROUNDS.CSV, voters param in database is replaced by first turn ID - 1 starts the game
    """

    # def __init__(self, player_id, swing, partisans, news, hype, cash, media, mojo, money):
    def __init__(self, player_params):
        self.id = player_params[0]  # 0 = Trump, 1 = Hillary;
        # 0 / 1 id is used to assign to Cards proper titles and images
        # note: for Cards, 0 is a code for 'voters' actions; voters is computed
        # column zero codes a player to keep other codes consistent between CSVs
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
        self.deck = None  # pointer to Deck that Player owns
        self.hand = None  # pointer to Hand that Player owns
        self.active = False  # Active Player plays the next Card
        self.human = False  # Human player == True gets HID input, False = algorithm plays
        self.winner = None

    def __str__(self):  # string method for class
        return self.name

    def status(self):  # extended printout of player parameters to console
        str1 = '{} has {} voters, of them {} swing voters and {} partisans, {} news, {} hype, {} cash, {} media, {} mojo, {} money.'
        str2 = ''
        if self.active == False:
            str2 = '{} waits for turn'.format(self.name)
        elif self.active == True:
            str2 = '{} makes next turn'.format(self.name)
        return str1.format(self.name, self.swing + self.partisans, self.swing, self.partisans, self.news, self.hype,
                           self.cash,
                           self.media, self.mojo, self.money) + '\n' + str2

    def set_deck(self, deck):
        self.deck = deck

    def set_hand(self, hand):
        self.hand = hand

    def get_hand(self):
        return self.hand

    def get_player_data(self, data_id):  # returns a single paramenter by name or id, needed to check card playablility
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

    def get_player_id(self):
        # fast player id retrieval
        return self.id

    def get_resources(self):
        # fast check of card playability; zero added to account for free cards
        return [0, self.news, self.hype, self.cash]

    def set_resources(self, type, value):
        # COLOR COST: when a card is played, it 'pays' its resource price
        if type == 0:
            if value == 99:  # THREE COLOR the priciest killer card
                self.news -= value
                self.hype -= value
                self.cash -= value
            else:  # GREY free cards
                pass
        elif type == 1:  # RED news cards
            self.news -= value
        elif type == 2:  # BLUE hype cards
            self.hype -= value
        elif type == 3:  # GREEN cash cards
            self.cash -= value
        else:
            print 'Card cost type is not recognized!'

    def update_resources(self):  # at the end of turn, update resources of players
        self.news += self.media
        self.hype += self.mojo
        self.cash += self.money

    def card_action(self, value, action_type):
        # card arguments modify player data per appropriate resource id, probably easiest way
        if action_type == 0:
            # voters = swing + partisans, min value = 0;
            # if damage greater than swing voters, only then partisans are damaged by the remainder
            # add voters branch
            if value > 0:
                self.swing += value
            # lose voters branch
            elif value < 0:
                self.partisans = max(0, self.partisans + self.swing + value)
                self.swing = max(0, self.swing + value)
            else:
                pass
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
        elif action_type == 11:  # new turn, nothing is changed, Card already changed everything
            pass
        else:
            print 'invalid action type, must be 0...11'
            pass

    def get_active(self):
        """Active player plays the next card"""
        return self.active

    def set_active(self, true_false):

        self.active = true_false

    def set_winner(self, true_false):
        """End of game states. True == Player won the game; False == lost"""
        self.winner = true_false

    def reset(self):
        """method for testing only; returns player to some hard coded base state"""
        self.swing = 0
        self.partisans = 0
        self.news = 0
        self.hype = 0
        self.cash = 0
        self.media = 4
        self.mojo = 4
        self.money = 4


class Card:
    """CONTAINER FOR CARD PARAMETERS
    for the time being Trump and Hillary use the same card values with different names
    """

    def __init__(self, player, opponent, deck, card_params):
        # csv is processed outside Card, Card is fed params already as a dict
        self.player = player
        self.opponent = opponent
        self.deck = deck  # Deck that Card belongs to
        # process card_params
        self.card_id = card_params['id']
        self.description = card_params['descr'].replace('*', '; ')
        # !! reference by id seems excessive
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
        # set actions and ignore empty actions
        self.action1 = [card_params['act1_value'], card_params['act1_type'], card_params['act1_side']]
        if card_params['act2_value'] == 0:
            self.action2 = None
        else:
            self.action2 = [card_params['act2_value'], card_params['act2_type'], card_params['act2_side']]
        if card_params['act3_value'] == 0:
            self.action3 = None
        else:
            self.action3 = [card_params['act3_value'], card_params['act3_type'], card_params['act3_side']]
        self.playable = False  # Only Hand can declare a Card playable; True if player's resource equal or greater than cost
        self.inplay = False  # Only Hand can declare a Card in play, one at a time

    def __repr__(self):
        return '{0} = {4}{1} ({2}/{3})'.format(self.card_id, self.name, self.cost_color, self.cost_value,
                                               '-!-' if self.playable else '')
        # return 'name = ' + str(self.name) + '\n color = ' + str(self.cost_color) + '\n cost = ' + str(self.cost_value) + '\n action3 = ' + str(self.action3)

    def play(self):
        # subtracts card resources
        self.player.set_resources(self.cost_color, self.cost_value)
        # changes turn order: player inactive, opp active
        self.player.set_active(0)
        self.opponent.set_active(1)
        # action 1
        if self.action1[2] == 0:
            self.player.card_action(self.action1[0], self.action1[1])
        elif self.action1[2] == 1:
            self.opponent.card_action(self.action1[0], self.action1[1])
        elif self.action1[2] == 2:
            self.player.card_action(self.action1[0], self.action1[1])
            self.opponent.card_action(self.action1[0], self.action1[1])
        # action 2
        if self.action2 is None:
            pass
        elif self.action2[2] == 0:
            if self.action2[1] == 11:
                print 'Card creates free turn in Action 2'
                self.player.set_active(1)
                self.opponent.set_active(0)
            else:
                self.player.card_action(self.action2[0], self.action2[1])
        elif self.action2[2] == 1:
            self.opponent.card_action(self.action2[0], self.action2[1])
        elif self.action2[2] == 2:
            self.player.card_action(self.action2[0], self.action2[1])
            self.opponent.card_action(self.action2[0], self.action2[1])
        # action 3
        if self.action3 is None:
            pass
        elif self.action3[2] == 0:
            if self.action3[1] == 11:
                print 'Card creats free turn in Action 3'
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
            if self.action2 is None:
                return ''
            else:
                return self.action2
        elif action_id == 3:
            if self.action3 is None:
                return ''
            else:
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
    """LIST OF CARDS AND INPUT-OUTPUT OPERATIONS
    Deck contains Player-specific Cards, one Deck for each Player"""

    def __init__(self):
        self.cards = []
        self.player = None
        self.hand = None  # Pointer to Hand to which Deck deals Cards

    def __str__(self):
        return 'Deck owner - {}'.format(str(self.player)) + '\n {}'.format('\n '.join(map(str, self.cards)))

    def set_hand(self, hand):
        self.hand = hand

    def set_player(self, player):
        self.player = player

    def shuffle(self):
        random.shuffle(self.cards)

    def pop_card(self):
        """Pulls the first Card out of the Deck; normally passes it it Hand"""
        return self.cards.pop()

    def append(self, card):
        """Adds a Card to the Deck"""
        self.cards.append(card)

    def not_empty(self):
        """mostly for testing, probably not needed in the game"""
        if not self.cards:
            return False  # https://www.python.org/dev/peps/pep-0008/#id49
        else:
            return True


class Hand:
    """LIST OF CARDS ON PLAYING FIELD"""

    def __init__(self):
        # fixed length list always with 6 items
        # later might use deque instead -- https://docs.python.org/3/library/collections.html#deque-objects
        self.cards = []
        self.player = None
        self.deck = None
        # these lines ar just to supress validation warnings
        # they appear in set_playables when 0 are addressed as Card class objects
        for i in range(6):
            self.cards.append(0)  # 0 stands for -here Card is missing-

    def __repr__(self):
        # return '[%s]' % '\n '.join(map(str, self.cards))
        # return '\n '.join(map(str, self.cards))
        return 'Hand owner - {}'.format(str(self.player)) + '\n {}'.format('\n '.join(map(str, self.cards)))

    def set_player(self, player):
        self.player = player

    def set_deck(self, deck):
        self.deck = deck

    def take_card(self, card):
        """Adds a Card to Hand in place of 0
        universal method, works both at start and in game"""
        for i in range(6):
            if 0 not in self.cards:
                print 'Hand.take_card says: {} Hand full!'.format(self.player)
            else:  # else == previous if is False
                if self.cards[i] == 0:
                    # insert Card once and stop!
                    self.cards[i] = card
                    break  # interrupts FOR loop after the first occurence is found

    def refill(self):  # checks for blanks and replaces them with valid Cards
        for i in range(6):
            if self.cards[i] == 0:
                self.cards[i] = self.deck.pop_card()

    def set_playables(self):
        """Resets playability at the end of player's turn, assumes 6 cards !!
        Validation here raises errors because self.cards init as list of INT, not Card obj """
        res = self.player.get_resources()
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

    def get_playable_cards(self):  # returns a list of playable Cards; can be empty!
        playable_cards = []
        print '{} - {}'.format(self.player, self.cards)
        for n in self.cards:
            if n == 0:
                pass
            elif n.get_playable():
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

    def index_playable(self):  # returns a list of indices of playable cards only
        index = []
        for i in range(6):
            if self.list_playable()[i]:
                index.append(i)
        # prev version, gave errors on empty cards
        # for i in range(6):
        #     if self.cards[i].get_playable():
        #         index.append(i)
        return index

    def play_random_card(self):
        playable_cards_indices = self.index_playable()
        if not playable_cards_indices:  # ATT !! Discard not implemented
            print 'Hand.play_random_card says: {} has no playable cards, GM will pass the turn'.format(self.player)
        else:
            index = random.choice(playable_cards_indices)
            active_card = self.cards[index]
            self.cards[index] = 0
            print 'Hand.play_random_card prepares to play card {}'.format(active_card)
            active_card.play()
            self.deck.append(active_card)

    def play_discard_random_card(self):
        playable_cards_indices = self.index_playable()
        if not playable_cards_indices:  # discard a card and pass a turn
            print 'Hand.play_random_card says: {} has no playable cards, will discard a random card'.format(self.player)
            index = random.choice(range(6))
            active_card = self.cards[index]
            print 'Preparing to discard {}'.format(active_card)
            active_card.get_player().set_active(False)
            active_card.get_opponent().set_active(True)
            self.cards[index] = 0
            self.deck.append(active_card)  # becomes card 1
            self.deck.shuffle()  # get rid of this
            print '{}'.format(self.cards)
            print 'Hand.play_random_card says: player {} set to {}'.format(self.player, self.player.get_active())
        else:
            index = random.choice(playable_cards_indices)
            active_card = self.cards[index]
            self.cards[index] = 0
            print 'Hand.play_random_card says: {} prepares to play card {}'.format(self.player, active_card)
            active_card.play()
            self.deck.append(active_card)  # becomes card 1
            self.deck.shuffle()  # get rid of this

    def play_selected_card(self, card_index):
        """Plays a Card referred by card_index; 0-5 index of card in deck
        Validation here raises errors because self.cards init as list of INT, not Card obj """
        card = self.cards[card_index]
        if card.get_playable():
            self.cards[card_index] = 0
            card.set_inplay(True)
            card.play()
        else:
            print 'This card is not playable, enter new card'
            self.play_selected_card(self, raw_input('enter a new card id'))

            # ** THE END **
