import posix
from ssl import TLSVersion

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
from itertools import chain
from typing import NamedTuple

class RobotGrid(Grid):
    DIRECTION_MAP = {
        "<": DIRECTIONS.LEFT.value,
        ">": DIRECTIONS.RIGHT.value,
        "v": DIRECTIONS.DOWN.value,
        "^": DIRECTIONS.UP.value
    }

    def __init__(self, grid):
        super().__init__(grid)

        n_rows, n_cols = self.dims()

        for row in range(n_rows):
            for col in range(n_cols):
                current = Coordinate(row, col)

                if self[current] == "@":
                    self.robot = current
                    return

    def push(self, char_direction, item=None):
        # move pointer along direction, and collect items into collected
        # and set them to ".". When we hit a wall or an empty space, then
        # unpack collected items from pointer

        # Stop if pointer is "." or "#"
        #     if "#", then move -1 direction

        # Collect item on pointer
        # Set item at pointer to "."
        # move pointer + 1 direction

        direction = RobotGrid.DIRECTION_MAP[char_direction]
        stop_items = {'.', '#'}

        collected = []

        if not item:
            item = self.robot

        update_robot = item == self.robot

        pointer = item
        front = item

        while self[pointer] not in stop_items:
            collected.append(self[pointer])
            self[pointer] = "."
            pointer += direction

        if self[pointer] == '.':
            pointer += direction

        while collected:
            pointer -= direction
            front = collected.pop()
            self[pointer] = front

        if update_robot:
            self.robot = pointer

    def get_GPS_coord_total(self):
        total = 0
        for row_idx, row in enumerate(self.grid):
            for col_idx, char in enumerate(row):
                if char == "O":
                    total += row_idx * 100 + col_idx

        return total

class RobotGrid2(RobotGrid):

    def __init__(self, grid):
        new_grid = []

        for row in grid:
            new_row = []
            for char in row:
                if char == "#":
                    new_row += ["#"] * 2
                elif char == "O":
                    new_row += ["[", "]"]
                elif char == ".":
                    new_row += ["."] * 2
                elif char == "@":
                    new_row += ["@", "."]
                else:
                    raise ValueError(f'Unexpected character {char} encountered')

            new_grid.append(new_row)

        super().__init__(new_grid)

    def can_push(self, coordinate, direction):
        forward = coordinate + direction

        if self[forward] == "#":
            return False
        elif self[forward] in {"[", "]"}:
            if self[forward] == "[":
                alternate = forward + DIRECTIONS.RIGHT.value
            else:
                alternate = forward + DIRECTIONS.LEFT.value
            return self.can_push(forward, direction) and self.can_push(alternate, direction)
        elif self[forward] == ".":
            return True
        else:
            raise ValueError(f"Unexpected handling fpr {self[forward]}")

    def push(self, char_direction, item=None):
        if not item:
            item = self.robot

        if char_direction in {'<', '>'}:
            super().push(char_direction)
        else:
            direction = RobotGrid.DIRECTION_MAP[char_direction]
            forward = item + direction
            if self[forward] in {"[", "]"}:
                if self[forward] == "[":
                    alternate = forward + DIRECTIONS.RIGHT.value
                else:
                    alternate = forward + DIRECTIONS.LEFT.value

                if self.can_push(forward, direction) and self.can_push(alternate, direction):
                    self.push(char_direction, forward)
                    self.push(char_direction, alternate)
                    super().push(char_direction, item)
            else:
                super().push(char_direction, item)



    def get_GPS_coord_total(self):
        total = 0
        for row_idx, row in enumerate(self.grid):
            for col_idx, char in enumerate(row):
                if char == "[":
                    total += row_idx * 100 + col_idx

        return total


def main1_impl(tuple_):

    index = next(idx for idx, row in enumerate(tuple_) if row == "")

    grid = RobotGrid(tuple_[:index])

    moves = ''.join(tuple_[index+1:])

    for move in moves:
        grid.push(move)

    return grid.get_GPS_coord_total()

def main2_impl(tuple_):
    index = next(idx for idx, row in enumerate(tuple_) if row == "")

    grid = RobotGrid2(tuple_[:index])

    moves = ''.join(tuple_[index+1:])

    for move in moves:
        grid.push(move)


    return grid.get_GPS_coord_total()

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
