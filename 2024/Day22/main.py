import posix
from ast import literal_eval
from ssl import TLSVersion

from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS, GridPointer
from collections import Counter, deque
from functools import cmp_to_key, cache
from itertools import product, combinations
import re
import math
from typing import NamedTuple
from collections import defaultdict
import heapq
from itertools import chain
from typing import NamedTuple

MULT_VALUE = 2**6
DIVIDE_VALUE = 2**5
MULT_VALUE_2 = 2**11

PRUNE_VALUE = 2**24

def next_number(value):
    value = (value * MULT_VALUE) ^ value
    value = value % PRUNE_VALUE

    value = (value // DIVIDE_VALUE) ^ value
    value = value % PRUNE_VALUE

    value = (value * MULT_VALUE_2) ^ value
    value = value % PRUNE_VALUE

    return value

def get_2000th_number(value):
    for i in range(2000):
        value = next_number(value)

    return value

def get_sequence_values(value):
    sequences = dict()

    sequence = deque()
    current = value
    for i in range(2000):
        value = next_number(current)
        value_as_bananas = value % 10
        diff = value_as_bananas - current % 10

        current = value

        sequence.append(diff)

        if len(sequence) == 5:
            sequence.popleft()
            sequence_tup = tuple(sequence)

            if sequence_tup not in sequences:
                sequences[tuple(sequence)] = value_as_bananas

    return sequences

def main1_impl(tuple_):
    tuple_values = tuple(int(value) for value in tuple_)

    total = 0
    for value in tuple_values:
        val = get_2000th_number(value)
        total += val

    return total

def main2_impl(tuple_):

    tuple_values = tuple(int(value) for value in tuple_)

    sequence_results = []

    for value in tuple_values:
        sequence_results.append(get_sequence_values(value))

    total_keys = set()
    for sequence_result in sequence_results:
        total_keys.update(sequence_result.keys())

    current_best = 0

    for key in total_keys:
        total = 0
        for sequence_result in sequence_results:
            if key in sequence_result:
                total += sequence_result[key]

        current_best = max(total, current_best)

    return current_best

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
