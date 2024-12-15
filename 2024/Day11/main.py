from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS, GridPointer
from collections import Counter
from functools import cmp_to_key
from itertools import product, combinations
import re
import math
from typing import NamedTuple
from collections import defaultdict
import heapq
from functools import cache
from itertools import chain

@cache
def get_stones(value, n_blinks):
    val_str = str(value)

    val_len = len(val_str)

    val_len_2 = val_len // 2

    if n_blinks == 1:
        if value == 0:
            return (1, )
        elif val_len % 2 == 0:
            return int(val_str[:val_len_2]), int(val_str[val_len_2:])
        else:
            return (value * 2024, )
    else:
        if value == 0:
            return get_stones(1, n_blinks - 1)
        elif val_len  % 2 == 0:
            return get_stones(int(val_str[:val_len_2]), n_blinks - 1) + get_stones(int(val_str[val_len_2:]), n_blinks - 1)
        else:
            return get_stones(value * 2024, n_blinks - 1)

def get_stones_single(counter):
    new_counter = Counter()
    for key, value in counter.items():

        val_str = str(key)
        val_len = len(val_str)
        val_len_2 = val_len // 2

        if key == 0:
            new_counter[1] += value
        elif val_len % 2 == 0:
            new_counter[int(val_str[:val_len_2])] += value
            new_counter[int(val_str[val_len_2:])] += value
        else:
            new_counter[key * 2024] += value

    return new_counter

def main1_impl(tuple_):
    all_values = tuple(map(int, tuple_[0].split()))

    stones_counter = Counter(all_values)

    for i in range(25):
        stones_counter = get_stones_single(stones_counter)

    total = 0

    for key, value in stones_counter.items():
        total += value

    return total

def main2_impl(tuple_):
    all_values = tuple(map(int, tuple_[0].split()))

    stones_counter = Counter(all_values)

    for i in range(75):
        stones_counter = get_stones_single(stones_counter)

    total = 0

    for key, value in stones_counter.items():
        total += value

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
