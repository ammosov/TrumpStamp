from player import Player
from random import randint
from kivy.logger import Logger
import time

TO_PRESS = 228
TO_DROP = 265


class AbstractBot(Player):

    def analysis(self, game_info):
        pass

    def set_active(self, active):
        print 'bot set active called with ', active
        self.active = active
        if not self.active:
            return
        Logger.info('bot set active')
        Logger.info(str(self.player_name))
        game_info = {
            'partisans': self.partisans,
            'swing': self.swing,
            'media': self.media,
            'news': self.news,
            'mojo': self.mojo,
            'hype': self.hype,
            'money': self.money,
            'cash': self.cash,
            'cards': self.hand.cards,

            'opp_partisans': self.opponent.partisans,
            'opp_swing': self.opponent.swing,
            'opp_media': self.opponent.media,
            'opp_news': self.opponent.news,
            'opp_mojo': self.opponent.mojo,
            'opp_hype': self.opponent.hype,
            'opp_money': self.opponent.money,
            'opp_cash': self.opponent.cash,
            'opp_cards': self.opponent.hand.cards
        }

        card, action = self.analysis(game_info)  # this function gives card and action, which we have to use on it

        if action == TO_PRESS:
            card.on_press()
        elif action == TO_DROP:
            card.on_drop()


class DropBot(AbstractBot):

    def analysis(self, game_info):
        return game_info['cards'][0], TO_DROP


class RandomDropBot(AbstractBot):

    def analysis(self, game_info):
        return game_info['cards'][randint(0, 6)], TO_DROP


def getResourceName(color):
    if color == 1:
        return 'news'
    if color == 2:
        return 'cash'
    if color == 3:
        return 'hype'


class RandomPressDrop(AbstractBot):

    '''
    available_cards_indices -- numbers of cards in this.hand.cards, which we can use.
    and return some random available card with label TO_PRESS, if that is possible, otherwise we
    return some random card with label TO_DROP
    '''

    def analysis(self, game_info):
        available_cards_indices = []
        for card_index in range(len(game_info['cards'])):
            card = game_info['cards'][card_index]
            cost_color, cost_value = card.get_cost()
            if cost_color == 0:
                available_cards_indices.append(card_index)
                continue
            resource_name = getResourceName(cost_color)
            if game_info[resource_name] >= cost_value:
                available_cards_indices.append(card_index)

        if len(available_cards_indices) > 0:
            random_index = available_cards_indices[randint(0, len(available_cards_indices)-1)]
            return game_info['cards'][random_index], TO_PRESS

        return game_info['cards'][randint(0, 6)], TO_DROP


