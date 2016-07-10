# collection of deck related functions and snippets

types = (' Voters ', ' Swing Voters ', ' Partisans ',
         ' News ', ' Emotions ', ' Money ',
         ' Media ', ' Charisma ', ' Funds ')
per_turn = ' per turn'
sides = ('to you', 'to opp', 'to both')


'''
LOCALIZATION SUPPORT !!
'''


def label_line(value, act_type, side):
    """
    Generates a label line from value and strings
    format = [value][voter or resource type][per turn or not][to whom]
    value - INT, require
    type - INT in range(8) - per types tuple, required
    side - INT in range(2) - per side type, required
    """
    lbl_val = '{0:+}'.format(value)  # card value is formatted with a sign as -1|+1
    lbl_type = types[act_type]  # from types tuple, take a specific label
    lbl_side = sides[side]  # from sides tuple, take a specific label

    if value == 0:  # check if there is action at all
        return None
    else:
        return lbl_val + lbl_type + lbl_side


def label_multline(act0, act1, act2):
    """
    Generates a label from card values
    assumes actX tuples eg (12,1,0),(9,0,0),(4,4,1)
    """
    card_label = ''  # init empty label

    # split in actions

    card_label += label_line(act0[0], act0[1], act0[2])

    # check if second action exists and process
    if act1 is None:
        return card_label
    else:
        card_label = card_label + '\n' + label_line(act1[0], act1[1], act1[2])
        # check if third action exists and process
        if act2 is None:
            return card_label
        else:
            card_label = card_label + '\n' + label_line(act2[0], act2[1], act2[2])
            return card_label

# TEST ZONE

print label_multline((5, 1, 0), (5, 2, 0), (- 1, 7, 0))

# correct -- +5 Swing Voters to you +5 Partisans to you -1 Charisma to you
