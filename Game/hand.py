"""Hand module."""
import os

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


class Hand():
    """Hand class."""

    POSITIONS_X = {0: list(map(lambda x: x / 2048.0, [522, 790, 1058, 1326, 1594, 1862])),
                   1: list(map(lambda x: x / 2048.0, [182, 450, 718, 986, 1254, 1522]))}
    POSITIONS_Y = {0: (1536.0 - 1488.0) / 1536.0,
                   1: (1536.0 - 150.0) / 1536.0}

    def __init__(self, deck):
        """Init hand."""
        self.deck = deck
        self.player = deck.get_owner()
        self.cards = [None] * 6

    def pop_card(self, popped_card):
        """Remove card from hand."""
        for i in xrange(len(self.cards)):
            if self.cards[i] == popped_card:
                self.cards[i] = None
    """
    def render_cards(self):
        for i, card in enumerate(self.cards):
            card.pos_hint = {'x': self.POSITIONS_X[self.player.player_id][i],
                             'y': self.POSITIONS_Y[self.player.player_id]}
            card.render()
    """
    def card_in_hand(self, card):
        """Check if card is in hand."""
        return card in self.cards

    def render_cards(self):
        """Render hand cards."""
        self.update_available_cards()
        for i, card in enumerate(self.cards):
            if self.player.active:
                card.show()
            else:
                card.hide()
            pos_hint = {'center_x': self.POSITIONS_X[self.player.player_id][i]}
            if self.player.player_id == 1:
                pos_hint['top'] = self.POSITIONS_Y[1]
            else:
                pos_hint['y'] = self.POSITIONS_Y[0]
            card.pos_hint = pos_hint
            card.render()

    def refill(self):
        """Refill hand.

        Draw missing cards from deck.
        """
        for i in xrange(len(self.cards)):
            if not self.cards[i]:
                new_card = self.deck.pop_card()
                self.cards[i] = new_card

    def update_available_cards(self):
        """Update opacity of cards.

        Make unavailable cards transparent.
        """
        print('updating cards')
        # print("cash: {}, hype: {}, news: {}".format(cash, hype, news))
        if not self.player.is_bot():
            for card in self.cards:
                if card:
                    cost_color, cost_value = card.get_cost()
                    if cost_color != 0 and cost_color != 4:
                        property_value = self.player.property(
                                         self.player.RESOURSES[cost_color]).get(self.player)
                        if property_value < cost_value:
                            card.set_disabled()
                            print("Disabled card " + str(card))
                        else:
                            card.set_enabled()
                            print("Enabled card " + str(card))
                    elif cost_color == 4:
                        hype_value = self.player.property('hype').get(self.player)
                        news_value = self.player.property('news').get(self.player)
                        cash_value = self.player.property('cash').get(self.player)
                        if (news_value < cost_value and hype_value < cost_value and
                                cash_value < cost_value):
                            card.set_disabled()
                            print("Disabled card " + str(card))
                        else:
                            card.set_enabled()
                            print("Enabled card " + str(card))
