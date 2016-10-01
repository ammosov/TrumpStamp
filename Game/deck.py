"""Deck module."""
import kivy
import random
kivy.require('1.7.2')


class Deck():
    """Deck class."""

    def __init__(self, player, card_factory):
        """Init deck."""
        self.player = player
        self.cards = [card_factory.get_card(i, player.get_player_id()) for i in xrange(1, 54)]
        self.discard = []

    def get_owner(self):
        """Return deck owner."""
        return self.player

    def shuffle(self):
        """Shuffle cards."""
        random.shuffle(self.cards)

    def pop_card(self):
        """Remove card from deck."""
        if len(self.cards) == 0:
            self.cards = self.discard[:]
            self.discard = []
            self.shuffle()
            print "New deck!"
            print "Cards:", self.cards
            print "Discard:", self.discard
        return self.cards.pop()

    def drop_card(self, card):
        """Drop card.

        Played cards should be in discard too.
        """
        self.discard.append(card)
