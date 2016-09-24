class Hand():
    POSITIONS_X = [34 / 2048.0, 302 / 2048.0, 570 / 2048.0, 838 / 2048.0, 1106 / 2048.0, 1374 / 2048.0]
    POSITIONS_Y = {0: (1536.0 - 1488.0) / 1536.0,
                   1: (1536.0 - 488.0) / 1536.0}

    def __init__(self, deck):
        self.deck = deck
        self.cards = [None] * 6

    def pop_card(self, popped_card):
        for i in xrange(len(self.cards)):
            if self.cards[i] == popped_card:
                self.cards[i] = None

    def render_cards(self):
        owner_id = self.deck.get_owner().player_id
        for i, card in enumerate(self.cards):
            card.pos_hint = {'x': self.POSITIONS_X[i],
                             'y': self.POSITIONS_Y[owner_id]}

    def refill(self):
        for i in xrange(len(self.cards)):
            if not self.cards[i]:
                self.cards[i] = self.deck.pop_card()
        self.render_cards()