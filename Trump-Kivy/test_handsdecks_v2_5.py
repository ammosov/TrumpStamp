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

# Shuffle decks
td.shuffle()
hd.shuffle()

# Init Hands
th = Hand(0)
hh = Hand(1)
# Set Hand owners
th.set_player(trump)
hh.set_player(hillary)
# fill initial Hands
for i in range(6):
    th.take_card(td.pop_card())
    hh.take_card(hd.pop_card())

# TEST OF DECK AND HAND FUNCTIONS


# Verify that players were created properly
print trump.status()
print hillary.status()

# print Decks
print 'Trump deck - \n {}'.format(th)
print 'Hillary deck - \n {}'.format(hh)
print trump.get_resources()
print hillary.get_resources()

# check playability

th.set_playables()
hh.set_playables()

# print Hands and Decks
print '{} \n\n {}'.format(th, td)
print '\n\n'
print '{} \n\n {}'.format(hh, hd)

