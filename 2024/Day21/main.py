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

def bisect_sequence(key_list):
    end = len(key_list)

    A_counting = False

    counter = Counter()
    pointer = 0

    indexes = [0]

    while pointer < end:

        if A_counting and key_list[pointer] != 'A':
            A_counting = False
            indexes.append(pointer)
        else:
            if key_list[pointer] == '^':
                counter['up'] += 1
            elif key_list[pointer] == 'v':
                counter['up'] -= 1
            elif key_list[pointer] == '<':
                counter['right'] -= 1
            elif key_list[pointer] == '>':
                counter['right'] += 1
            elif key_list[pointer] == 'A':
                if counter['up'] == 0 and counter['right'] == 0:
                    A_counting = True
            else:
                raise ValueError(f'Unexpected character {key_list[pointer]}')

            pointer += 1

    indexes.append(end)
    middleIndex = len(indexes) // 2

    return indexes[middleIndex]


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

        return total_sequence

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
        if key_list in Robotpad._cache:
            return Robotpad._cache[key_list]

        mid_idx = bisect_sequence(key_list)

        if mid_idx != len(key_list): # Found a midpoint
            joined = self.sequence_from_list(key_list[:mid_idx]) + self.sequence_from_list(key_list[mid_idx:])
            Robotpad._cache[key_list] = joined
            return joined

        total_sequence = tuple()
        for key in key_list:
            total_sequence += self.sequence_for_key(key) + ('A', )

        Robotpad._cache[key_list] = total_sequence

        return total_sequence

def four_robot_control_sequence(code, n_robots) -> tuple:

    keypad_robot = Keypad() # Translates code in robotpad inputs

    code = keypad_robot.sequence_from_list(code)

    for i in range(n_robots):
        robotpad_robot = Robotpad()
        code = robotpad_robot.sequence_from_list(code)
        print(len(code))

    return code

def main1_impl(tuple_):

    codes = tuple_

    total = 0
    for code in codes:
        sequence = four_robot_control_sequence(code, 2)
        print(len(sequence))
        total += int(code[:3]) * len(sequence)

    return total


def main2_impl(tuple_):

    codes = tuple_

    total = 0
    for code in codes:
        sequence = four_robot_control_sequence(code, 25)
        print(len(sequence))
        total += int(code[:3]) * len(sequence)

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
