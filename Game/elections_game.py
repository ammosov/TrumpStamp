import kivy
import pandas as pd
import os
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label

from card import CardFabric
from kivy.animation import Animation
from player import Player
from bots import *

kivy.require('1.7.2')

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

round_csv = os.path.join(SCRIPT_DIR, 'rounds.csv')
cards_csv = os.path.join(SCRIPT_DIR, 'cards.csv')


class ElectionsGame(FloatLayout):
    """
       This class represents the game.
       As a Kivy object it represents the game field and is a root for all other
       objects. As a general class it stores all the stuff in the game.
    """
    def __init__(self, **kwargs):
        super(ElectionsGame, self).__init__(**kwargs)
        round_id = 0
        self.trump = self.ids['trump_player']
        self.hillary = RandomPressDrop(self.ids['hillary_player'])
        self.PLAYERS = {0: self.trump,
                        1: self.hillary}
        self.card_fabric = CardFabric(self, cards_csv)
        round_db = pd.DataFrame(pd.read_csv(round_csv))
        self.victory = {'destr': round_db['destr'][round_id], 'res': round_db['res'][round_id]}
        # CREATE PLAYERS
        # parameters are labeled as t0-t1, digit points to resource code per card database
        self.trump.late_init(
            player_id=0,
            swing=round_db['t1'][round_id],
            partisans=round_db['t2'][round_id],
            news=round_db['t3'][round_id],
            hype=round_db['t4'][round_id],
            cash=round_db['t5'][round_id],
            media=round_db['t6'][round_id],
            mojo=round_db['t7'][round_id],
            money=round_db['t8'][round_id],
            card_fabric=self.card_fabric)
        self.hillary.late_init(
            player_id=1,
            swing=round_db['h1'][round_id],
            partisans=round_db['h2'][round_id],
            news=round_db['h3'][round_id],
            hype=round_db['h4'][round_id],
            cash=round_db['h5'][round_id],
            media=round_db['h6'][round_id],
            mojo=round_db['h7'][round_id],
            money=round_db['h8'][round_id],
            card_fabric=self.card_fabric)

        self.hillary.set_updaters(self.ids, 'hillary_player')

        self.trump.set_opponent(self.hillary)
        self.hillary.set_opponent(self.trump)

        if round_db['turn'][round_id]:
            self.trump.set_active(False)
            self.hillary.set_active(True)
        else:
            self.trump.set_active(True)
            self.hillary.set_active(False)

        # shuffle Decks
        self.trump.get_deck().shuffle()
        self.hillary.get_deck().shuffle()

        # deal 6 Cards from Decks to Hands
        self.trump.get_hand().refill()
        self.trump.get_hand().render_cards()
        self.hillary.get_hand().refill()
        self.hillary.get_hand().render_cards()

    def end_game(self):
        """Sets both Players to active=False to prevent playing further cards"""
        self.trump.set_active(False)
        self.hillary.set_active(False)
        print 'END GAME'

    def declare_victory(self):
        """checks if victory is achieved
       !! Current problem - what if both players are hit with one card?"""
        #
        # Use any() function + 2 dictionaries of victory that are updated from card turn
        #
        if self.victory['destr'] == 1:  # destruction is true/false
            # if Trump wins
            if self.hillary.get_voters() <= 0:
                self.trump.set_winner(True)
                print 'Trump won'
                return True
            # if Hillary wins
            elif self.trump.get_voters() <= 0:
                self.hillary.set_winner(True)
                print 'Hillary won'
                return True
            # No winner yet
            else:
                # print 'No winner yet'
                return False
        else:
            print 'No victory condition set!'

    def card_clicked(self, card):
        player = self.PLAYERS[card.get_owner()]
        opponent = self.PLAYERS[abs(card.get_owner() - 1)]
        free_turn = False
        if player.get_active():
            print '\nBegin new turn'
            if not player.pay_for_card(*card.get_cost()):
                return False
            player.get_hand().pop_card(card)
            player.get_deck().drop_card(card) #even played card should be in discard 
            if player.is_bot():
                card.show()
            actions = card.get_actions()  # {'player': [(type, value)], 'opponent': [(type, value)]}
            for action in actions['player']:
                if player.apply_card(*action):
                    free_turn = True
            for action in actions['opponent']:
                opponent.apply_card(*action)

            if self.declare_victory():
                self.end_game()
                return True

            if free_turn:
                player.set_active(True)
            else:
                player.set_active(False)

            player.get_hand().refill()

            if free_turn:
                opponent.set_active(False)
            else:    
                opponent.update_resources()
                opponent.set_active(True)

            opponent.get_hand().render_cards()
            player.get_hand().render_cards()
            
            return True
        else:
            print 'Its not your turn!'
            return False

    def card_dropped(self, card):

        print 'dropped:', card
        player = self.PLAYERS[card.get_owner()]
        opponent = self.PLAYERS[abs(card.get_owner() - 1)]
        if player.get_active():
            player.get_hand().pop_card(card)
            player.get_deck().drop_card(card)
            player.set_active(False)
            player.get_hand().refill()
            opponent.update_resources()
            #opponent.get_hand().refill()
            opponent.set_active(True)
            player.get_hand().render_cards()
            opponent.get_hand().render_cards()
            return True
        return False
