from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS
from collections import Counter
from functools import cmp_to_key
import re

def is_valid(update, in_front_of_dict):
    for idx, elem in enumerate(update):
        for i in range(idx):
            if elem in in_front_of_dict and update[i] in in_front_of_dict[elem]:
                return False

    return True

def make_less_than_functor(in_front_of_dict):
    def less_than(val1, val2):
        # The comparison logic from less_than_impl
        if (val1 in in_front_of_dict and val2 in in_front_of_dict[val1]):
            return -1  # val1 is less than val2
        elif (val2 in in_front_of_dict and val1 in in_front_of_dict[val2]):
            return 1   # val1 is greater than val2
        return 0       # val1 and val2 are considered equal
    return less_than

def main1_impl(tuple_):

    empty = tuple(a for a, val in enumerate(tuple_) if val == '')

    orderings = tuple_[:empty[0]]

    updates = tuple_[empty[0]+1:]
    updates = tuple(tuple(map(int, update.split(','))) for update in updates)

    in_front_of_dict = dict()

    total = 0

    for ordering in orderings:
        value, before = tuple(map(int, ordering.split('|')))

        if value not in in_front_of_dict:
            in_front_of_dict[value] = set((before,))
        else:
            in_front_of_dict[value].add(before)

    for update in updates:
        if is_valid(update, in_front_of_dict):
            total += update[int((len(update) -1) / 2)]

    return total

def main2_impl(tuple_):

    empty = tuple(a for a, val in enumerate(tuple_) if val == '')

    orderings = tuple_[:empty[0]]

    updates = tuple_[empty[0]+1:]
    updates = tuple(tuple(map(int, update.split(','))) for update in updates)

    in_front_of_dict = dict()

    total = 0

    for ordering in orderings:
        value, before = tuple(map(int, ordering.split('|')))

        if value not in in_front_of_dict:
            in_front_of_dict[value] = set((before,))
        else:
            in_front_of_dict[value].add(before)

    for update in updates:
        if not is_valid(update, in_front_of_dict):
            update_ = sorted(update, key=cmp_to_key(make_less_than_functor(in_front_of_dict)))
            print(update_)
            total += update_[int((len(update_) -1) / 2)]

    return total

def main1(file):
    file_tuple = read_file(file)

    return main1_impl(file_tuple)

def main2(file):
    file_tuple = read_file(file)

    return main2_impl(file_tuple)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
