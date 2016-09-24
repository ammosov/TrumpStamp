from player import Player
from random import randint

TO_PRESS = 228
TO_DROP = 265

class AbstractBot(Player):

    def Analysis(self, game_info):
        pass

    def set_active(self):
        super(AbstractBot, self).__init__()
        game_info = {
            'partisans' : self.partisans,
            'swing' : self.swing,
            'media' : self.media,
            'news' : self.news,
            'mojo' : self.mojo,
            'hype' : self.hype,
            'money' : self.money,
            'cash' : self.cash,
            'cards' : self.hand.cards,

            'opp_partisans' : self.opponent.partisans,
            'opp_swing': self.opponent.swing,
            'opp_media': self.opponent.media,
            'opp_news': self.opponent.news,
            'opp_mojo': self.opponent.mojo,
            'opp_hype': self.opponent.hype,
            'opp_money': self.opponent.money,
            'opp_cash': self.opponent.cash,
            'opp_cards': self.opponent.hand.cards
        }

        card, action = self.analysis(game_info)          # this function gives card and action, which we have to use on it

        if action == TO_PRESS:
            card.on_press()
        elif action == TO_DROP:
            card.on_drop()

class DrobBot(AbstractBot):

    def Analysis(self, game_info):
        return game_info['cards'][0], TO_DROP

class RandomDropBot(AbstractBot):

    def Analysis(self, game_info):
        return game_info['cards'][randint(0, 6)], TO_DROP




