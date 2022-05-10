"""This module makes random choices from lists of guests and prizes and then makes a new dictionary pair of guest and
prize while deleting said pair from original lists
"""
from random import choice


def randomizer_main(lst_prizes):
    """This function takes two lists and dictionary and makes a new key-value pair in the given dictionary

    lst_guests: list

    return: tuple
    """
    winner = choice(lst_prizes)
    return winner
