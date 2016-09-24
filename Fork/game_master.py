import kivy
import pandas as pd
import os
from kivy.uix.floatlayout import FloatLayout
from card import Card, CardFabric
from player import Player
from kivy.logger import Logger
kivy.require('1.7.2')

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

round_csv = os.path.join(SCRIPT_DIR, 'rounds.csv')
cards_csv = os.path.join(SCRIPT_DIR, 'cards.csv')

class GameMaster():
    """This class represents the game. As a Kivy object it represents the game field and is a root for all other
    objects. As a general class it stores all the stuff in the game.
    """

    def __init__(self, trump, hillary, layout):
        round_id = 0
        self.trump = trump
        self.hillary = hillary
        self.layout = layout
        self.card_fabric = CardFabric(self, cards_csv)
        self.PLAYER = {0: self.trump, 1: self.hillary}
        round_db = pd.DataFrame(pd.read_csv(round_csv))
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
            voters=(round_db['t1'][round_id] + round_db['t2'][round_id]),
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
            voters=round_db['h1'][round_id] + round_db['h2'][round_id],
            card_fabric=self.card_fabric)

        self.trump.set_opponent(self.hillary)
        self.hillary.set_opponent(self.trump)

        if round_db['turn'][round_id]:
            self.trump.set_active(False)
            self.hillary.set_active(True)
        else:
            self.trump.set_active(True)
            self.hillary.set_active(False)


        # for i in id_list:
        #     card0 = Card(self.trump, self.hillary, self.trump.get_deck(), processing_functions.get_row(cards_db, i))
        #     self.trump.get_deck().append_card(card0)
        #     card1 = Card(self.hillary, self.trump, self.hillary.get_deck(), processing_functions.get_row(cards_db, i))
        #     self.hillary.get_deck().append_card(card1)
        
        # shuffle Decks
        self.trump.get_deck().shuffle()
        self.hillary.get_deck().shuffle()

        # deal 6 Cards from Decks to Hands
        self.trump.get_hand().refill()
        self.hillary.get_hand().refill()
        # self.trump.get_hand().set_playables()
        # self.hillary.get_hand().set_playables()

    def get_layout(self):
        return self.layout

    def card_clicked(self, card):
        player = self.PLAYER[card.get_owner()]
        opponent = self.PLAYER[abs(card.get_owner() - 1)]
        if player.get_active():
            if not player.pay_for_card(card.get_cost()):
                card.deny()
            else:
                player.get_hand().pop_card(card)
                card.move()
            actions = card.get_actions() # {'player': [(type, value)], 'opponent': [(type, value)]}
            for action in actions['player']:
                player.apply_card(action[0], action[1])
            for action in actions['opponent']:
                opponent.apply_card(action[0], action[1])
            #TODO
            # check on winner
            