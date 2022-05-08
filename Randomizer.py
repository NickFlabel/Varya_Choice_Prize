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
