from gameclasses_v2_7 import *

game = GameMaster(4)

print game


n = 5
while n > 0:
    print '\ntest 2_7: New turn {}'.format(5 - n)
    game.turn_if_discard()
    # game.turn_if_switch()
    n -= 1

