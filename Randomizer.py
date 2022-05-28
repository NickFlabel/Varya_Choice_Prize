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


def balance_prizes_to_guests(prize_list, guest_number):
    """This function takes the lest of prizes and number of guests and balance the number of prizes to the number
    of guests
    """
    prize_number = 0
    new_list = []

    for prize in prize_list:
        prize_number += prize[3]

    list_of_new_proportions = []

    if guest_number > 0:
        for prize in prize_list:
            if prize_number > 0:
                proportion = prize[3] / prize_number
            else:
                proportion = 1 / len(prize_list)
            list_of_new_proportions.append(proportion)
    else:
        for prize in prize_list:
            new_list.append(0)
        return new_list

    for prop in list_of_new_proportions:
        new_list.append(round(prop*guest_number))

    new_sum = 0

    for elem in new_list:
        new_sum += elem

    if new_sum < guest_number:
        new_list[0] += 1
    elif new_sum > guest_number:
        new_list[-1] -= 1

    return new_list
