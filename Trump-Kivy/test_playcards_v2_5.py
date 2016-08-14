from gameclasses_v2_5 import *

# EVERYTHING BELOW IS FOR TESTING AND MIST BE DELETED AT END
# TEST OF CREATE_ROUND() and Player class

# can: create Cards, Decks, Hands, move Cards btw Deck and Hands

card_lists = range(1, 53),[99]  # put in round config

# Init players
trump, hillary = create_round(1)
players = (trump, hillary)
# Generate decks
td, hd = create_decks(players, card_lists)
# td, hd = create_simple_decks(players, card_lists)

# TEST OF CARDS BEING PROCESSED ACCURATELY

print 'TRUMP CARDS TEST'

trump.reset()
hillary.reset()
print '\n{}\n{}'.format(trump.status(), hillary.status())

# create 1 card
# crd = td.pop_card()
# crd = Card(trump, hillary, td, get_row(cards_db, 24))
# print 'Description: {}'.format(crd.get_description())

while td.not_empty():
    crd = td.pop_card()
    print '\nNew card: {}, owner {}, opponent {}'.format(crd, crd.get_player(), crd.get_opponent())
    print 'Description: {}'.format(crd.get_description())
    # play a card
    crd.play()
    print '\n{}\n{}'.format(trump.status(), hillary.status())
    trump.reset()
    hillary.reset()

print 'HILLARY CARDS TEST'

while hd.not_empty():
    crd = hd.pop_card()
    print '\nNew card: {}, owner {}, opponent {}'.format(crd, crd.get_player(), crd.get_opponent())
    print 'Description: {}'.format(crd.get_description())
    # play a card
    crd.play()
    print '\n{}\n{}'.format(trump.status(), hillary.status())
    trump.reset()
    hillary.reset()



