from gameclasses import *

# EVERYTHING BELOW IS FOR TESTING AND MIST BE DELETED AT END
# TEST OF CREATE_ROUND() and Player class

t, h = create_round(2)

print t.status()
print h.status()

card101 = Card(0,get_row(cards_db,47))
card201 = Card(1,get_row(cards_db,47))

print t.card_playable(card101.get_cost_color(), card101.get_cost_value())

t.card_action(25,5) # add cash

print t.status()
print t.card_playable(card101.get_cost_color(), card101.get_cost_value())

t.card_action(5,0) # add voters
print t.status()

t.card_action(5,1) # add swing voters
print t.status()

t.card_action(5,2) # add partisans
print t.status()

t.card_action(1,11) # set active turn
print t.status()
