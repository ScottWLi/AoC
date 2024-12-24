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

KEYPAD = [['7', '8', '9'],
          ['4', '5', '6'],
          ['1', '2', '3'],
          ['X', '0', 'A']]

ROBOTPAD = [['X', '^', 'A'],
            ['<', 'v', '>']]

COORDINATE_TO_STRING = {
    Coordinate(1, 0): 'v',
    Coordinate(0, 1): '>',
    Coordinate(0, -1): '<',
    Coordinate(-1, 0): '^'
}

def multiply_counter(counter, scalar):
    ret = Counter()

    for key, value in counter.items():
        ret[key] = value * scalar

    return ret

def count_sequence(key_list):
    end = len(key_list)

    A_counting = False

    local_counter = Counter()
    sequence_counter = Counter()

    start_pointer = 0
    end_pointer = 0

    indexes = [0]

    while end_pointer < end:

        if A_counting and key_list[end_pointer] != 'A':
            A_counting = False
            sequence_counter[key_list[start_pointer:end_pointer]] += 1
            start_pointer = end_pointer
        else:
            if key_list[end_pointer] == '^':
                local_counter['up'] += 1
            elif key_list[end_pointer] == 'v':
                local_counter['up'] -= 1
            elif key_list[end_pointer] == '<':
                local_counter['right'] -= 1
            elif key_list[end_pointer] == '>':
                local_counter['right'] += 1
            elif key_list[end_pointer] == 'A':
                if local_counter['up'] == 0 and local_counter['right'] == 0:
                    A_counting = True
            else:
                raise ValueError(f'Unexpected character {key_list[end_pointer]}')

            end_pointer += 1

    sequence_counter[key_list[start_pointer:end_pointer]] += 1

    return sequence_counter


def expand_coordinate(coordinate, horizontal_first=True, force_horizontal_first=False):
    n_rows = coordinate.row
    n_cols = coordinate.column

    if n_rows < 0:
        row_coordinate = Coordinate(-1, 0)
        n_rows = abs(n_rows)
    else:
        row_coordinate = Coordinate(1, 0)

    if n_cols < 0:
        col_coordinate = Coordinate(0, -1)
        n_cols = abs(n_cols)
    else:
        col_coordinate = Coordinate(0, 1)

    if force_horizontal_first:
        return (COORDINATE_TO_STRING[col_coordinate],) * n_cols + (COORDINATE_TO_STRING[row_coordinate],) * n_rows
    if not horizontal_first or col_coordinate == Coordinate(0,1):
        return (COORDINATE_TO_STRING[row_coordinate],) * n_rows + (COORDINATE_TO_STRING[col_coordinate],) * n_cols

    return (COORDINATE_TO_STRING[col_coordinate],) * n_cols + (COORDINATE_TO_STRING[row_coordinate],) * n_rows

class Keypad(Grid):
    def __init__(self):
        super().__init__(KEYPAD)
        self.pointer = self.find('A')

    def sequence_for_key(self, key: str) -> tuple:

        location = self.find(key)
        distance = location - self.pointer

        if distance and self.pointer.column == 0 and location.row == 3: # Start on Left column
            self.pointer = location
            return expand_coordinate(distance, True)

        elif distance and self.pointer.row == 3 and location.column == 0: # End on left column
            self.pointer = location
            return expand_coordinate(distance, False)

        self.pointer = location
        return expand_coordinate(distance)


    def sequence_from_list(self, key_list: tuple[str]) -> tuple:
        total_sequence = tuple()

        for key in key_list:
            total_sequence += self.sequence_for_key(key) + ('A',)

        return ''.join(total_sequence)

class Robotpad(Grid):
    _cache = {}
    def __init__(self):
        super().__init__(ROBOTPAD)
        self.A = self.find('A')
        self.pointer = self.A

    def sequence_for_key(self, key: str) -> tuple:

        location = self.find(key)
        distance = location - self.pointer

        if distance and self.pointer.column == 0: # Start on '<' key and need to move off at start
            self.pointer = location
            return expand_coordinate(distance, force_horizontal_first=True)

        elif distance and location.column == 0: # End on '<' key and need to move on at end
            self.pointer = location
            return expand_coordinate(distance, False)

        self.pointer = location
        return expand_coordinate(distance)

    def sequence_from_list(self, key_list: tuple[str]) -> tuple:
        total_sequence = tuple()
        for key in key_list:
            total_sequence += self.sequence_for_key(key) + ('A', )

        Robotpad._cache[key_list] = total_sequence

        return ''.join(total_sequence)

def _get_iterative_robot_calls(code_counter, n_calls):

    if n_calls > 0:
        code_counter = _get_iterative_robot_calls(code_counter, n_calls - 1)

    new_code_counter = Counter()

    for key, value in code_counter.items():
        breakdown = _cache_wrap_sequence_from_list_impl(key)
        new_code_counter.update(multiply_counter(breakdown, value))

    return new_code_counter

@cache
def _cache_wrap_sequence_from_list_impl(sequence):

    robotpad_robot = Robotpad()
    return count_sequence(robotpad_robot.sequence_from_list(sequence))

def four_robot_control_sequence(code, n_robots) -> Counter:

    keypad_robot = Keypad() # Translates code in robotpad inputs

    code = count_sequence(keypad_robot.sequence_from_list(code))

    return _get_iterative_robot_calls(code, n_robots-1)


def main2_impl(tuple_, n_robots=25):

    codes = tuple_

    total = 0
    for code in codes:
        sequence_counter = four_robot_control_sequence(code, n_robots)
        print(f"Final: {sequence_counter}")
        sequence_len = 0
        for key, values in sequence_counter.items():
            sequence_len += len(key) * values

        print(sequence_len)

        total += int(code[:3]) * sequence_len

    return total

def main1_impl(tuple_):

    return main2_impl(tuple_, 2)

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
