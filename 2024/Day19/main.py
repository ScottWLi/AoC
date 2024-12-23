import posix
from ast import literal_eval
from ssl import TLSVersion

from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS, GridPointer
from collections import Counter
from functools import cmp_to_key, cache
from itertools import product, combinations
import re
import math
from typing import NamedTuple
from collections import defaultdict
import heapq
from itertools import chain
from typing import NamedTuple

@cache
def can_make(pattern, towels):

    if not pattern:
        return True

    possibles = []
    for towel in towels:
        if pattern.startswith(towel):
            possibles.append(can_make(pattern[len(towel):], towels))

    return any(possibles)

@cache
def made_from(pattern, towels):

    if not pattern:
        return 1

    possibles = 0
    for towel in towels:
        if pattern.startswith(towel):
            possibles += made_from(pattern[len(towel):], towels)

    return possibles

def main1_impl(tuple_):

    towels = tuple(tuple_[0].split(', '))
    patterns = tuple_[2:]

    total = 0
    for pattern in patterns:
        if can_make(pattern, towels):
            total += 1

    return total


def main2_impl(tuple_):

    towels = tuple(tuple_[0].split(', '))
    patterns = tuple_[2:]

    total = 0
    for pattern in patterns:
        total += made_from(pattern, towels)

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
