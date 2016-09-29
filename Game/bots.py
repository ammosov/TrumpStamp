from player import Player
from random import randint
from kivy.logger import Logger

TO_PRESS = 228
TO_DROP = 265


class AbstractBot(Player):
    def __init__(self, *args, **kwargs):
        super(AbstractBot, self).__init__(**kwargs)

    def set_updaters(self, *args):
        if len(args) and isinstance(args[0], dict) and isinstance(args[1], str):
            player_id = args[1]
            # player = args[0][player_id]
            # print player_id, player
            # mapping = {'partisans': self.partisans,
            #            'swing': self.swing,
            #            'news': self.news,
            #            'hype': self.hype,
            #            'media': self.media,
            #            'mojo': self.mojo,
            #            'money': self.money,
            #            'cash': self.cash}
            # for key, prop in mapping.items():
            #     def updater(instance, value):
            #         args[0][player_id.replace('player','') + key].text = str(prop)
            #     updater(None, None)
            #     self.bind(**{key: prop})
            # BIND DOESN'T WORK INSIDE LOOPS. FUCK THIS FRAMEWORK!!!
            def upd_partisans(instance, value):
                args[0][player_id.replace('player', '') + 'partisans'].text = str(self.partisans)
            upd_partisans(None, None)
            self.bind(partisans=upd_partisans)
            def upd_swing(instance, value):
                args[0][player_id.replace('player', '') + 'swing'].text = str(self.swing)
            upd_swing(None, None)
            self.bind(swing=upd_swing)
            def upd_news(instance, value):
                args[0][player_id.replace('player', '') + 'news'].text = str(self.news)
            upd_news(None, None)
            self.bind(news=upd_news)
            def upd_hype(instance, value):
                args[0][player_id.replace('player', '') + 'hype'].text = str(self.hype)
            upd_hype(None, None)
            self.bind(hype=upd_hype)
            def upd_media(instance, value):
                args[0][player_id.replace('player', '') + 'media'].text = str(self.media)
            upd_media(None, None)
            self.bind(media=upd_media)
            def upd_cash(instance, value):
                args[0][player_id.replace('player','') + 'cash'].text = str(self.cash)
            upd_cash(None, None)
            self.bind(cash=upd_cash)
            def upd_mojo(instance, value):
                args[0][player_id.replace('player','') + 'mojo'].text = str(self.mojo)
            upd_mojo(None, None)
            self.bind(mojo=upd_mojo)
            def upd_money(instance, value):
                args[0][player_id.replace('player', '') + 'money'].text = str(self.money)
            upd_money(None, None)
            self.bind(money=upd_money)

    def analysis(self, game_info):
        pass

    def set_active(self, active):
        self.active = active
        if not self.active:
            return
        Logger.info('bot set active')
        self.play()

    def play(self):
        if not self.active:
            return
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

        print ('################')
        print ('opp cards:')
        for card in game_info['opp_cards']:
            print (card)
        print ('----------------')
        print ('bots cards:')
        for card in game_info['cards']:
            print (card)
        print ('################')
        card, action = self.analysis(game_info)  # this function gives card and action, which we have to use on it

        print ('bot made its choice')

        if action == TO_PRESS:
            card.use()
        elif action == TO_DROP:
            card.drop()


class DropBot(AbstractBot):

    def analysis(self, game_info):
        return game_info['cards'][0], TO_DROP


class RandomDropBot(AbstractBot):

    def analysis(self, game_info):
        return game_info['cards'][randint(0, 5)], TO_DROP


def getResourceName(color):
    if color == 1:
        return 'news'
    if color == 2:
        return 'cash'
    if color == 3:
        return 'hype'



class RandomPressBot(AbstractBot):

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
            if cost_value == 99:
                return game_info['cards'][card_index], TO_DROP
            if cost_color == 0:
                available_cards_indices.append(card_index)
                continue
            resource_name = getResourceName(cost_color)
            if game_info[resource_name] >= cost_value:
                available_cards_indices.append(card_index)

        if len(available_cards_indices) > 0:
            random_index = available_cards_indices[randint(0, len(available_cards_indices)-1)]
            return game_info['cards'][random_index], TO_PRESS

        return game_info['cards'][randint(0, 5)], TO_DROP


class GreedyBot(AbstractBot):

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

        self_coeff = -1
        enemy_coeff = 1
        if len(available_cards_indices) > 0:
            index = 0
            optimal_priority = 0
            for i in xrange(len(available_cards_indices)):
                priority = 0
                actions = game_info['cards'][available_cards_indices[i]].get_actions()
                for action in actions['player']:
                    if action[0] == 0:
                        priority += self_coeff * action[1]
                for action in actions['opponent']:
                    if action[0] == 0:
                        priority -= enemy_coeff * action[1]
                if i == 0:
                    optimal_priority = priority
                elif priority > optimal_priority:
                    index, optimal_priority = i, priority
            return game_info['cards'][available_cards_indices[index]], TO_PRESS
        else:
            index = 0
            for i in xrange(1, 5):
                if game_info['cards'][i].cost_value > game_info['cards'][index].cost_value:
                    index = i
            return game_info['cards'][index], TO_DROP
