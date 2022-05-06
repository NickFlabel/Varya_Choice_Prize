"""This module makes random choices from lists of guests and prizes and then makes a new dictionary pair of guest and
prize while deleting said pair from original lists
"""
from random import choice


def _random_choice(lst_guests, lst_prizes):
    """This function takes two lists and makes a random choice from each list and returns a tuple of a winner [0] and
    a prize [1]

    lst_guests: list
    lst_prizes: list

    returns: tuple (2 values - winner from the 1st list and a prize from the 2nd list)
    """
    try:
        return choice(lst_guests), choice(lst_prizes)  # It is worth making an exception if one of the lists if empty
    except IndexError:
        pass


def randomizer_main(lst_guests, lst_prizes):
    """This function takes two lists and dictionary and makes a new key-value pair in the given dictionary

    lst_guests: list
    lst_prizes: list
    winners: dict

    return: dict, tuple
    """
    winner = _random_choice(lst_guests, lst_prizes)
    return winner


def test():
    """This function tests the functions of this module
    """

    # 1st test of random_choice function

    lst1 = ['a', 'b', 'c']
    lst2 = [1, 2, 3]
    win = _random_choice(lst1, lst2)
    print(win)

    # 2nd test of deleting values from lists

    _delete_from_lists(win, lst1, lst2)
    if win[0] not in lst1 and win[1] not in lst2:
        print('Test 2 "Delete" test in ok')
    else:
        print('Test 2 "Delete" failed')

    # 3d test (appending dict)

    winners = {}
    for i in range(3):
        randomizer_main(lst1, lst2, winners)

    print(winners)

    # 4th test - % of success

    probability_mapper = {}

    for i in range(5000):
        guests = ['Nick Flabel', 'Flavius Belisarius', 'Andre Velan', 'Julianos Grelan', 'Squirrel']

        prizes = ['Flame Sword +3', 'Spellbook of Ruin', 'Orb of Deception']

        winners = {}

        for i in range(len(guests)):
            randomizer_main(guests, prizes, winners)

        for key in winners:
            probability_mapper.setdefault(key, 0)
            probability_mapper[key] += 1

    for key in probability_mapper:
        probability_mapper[key] = probability_mapper[key] / 5000 * 100

    for key in probability_mapper:
        print(key + ': ' + str(probability_mapper[key]) + ' %')
