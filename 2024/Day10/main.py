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

def find_trailhead_uniques(start, grid, trailheads):

    queue = [start]
    next = []
    for i in range(9):
        for coord in queue:
            for direction in DIRECTIONS.simple_directions():
                new_coord = coord + direction.value

                if new_coord in grid and grid[new_coord] == (i + 1):
                    next.append(new_coord)

        queue = next
        next = []

    # queue should now contain all coordinates with value 9

    for coord_9 in set(queue):
        trailheads[coord_9] += 1
def find_trailhead(start, grid, trailheads):

    queue = [start]
    next = []
    for i in range(9):
        for coord in queue:
            for direction in DIRECTIONS.simple_directions():
                new_coord = coord + direction.value

                if new_coord in grid and grid[new_coord] == (i + 1):
                    next.append(new_coord)

        queue = next
        next = []

    # queue should now contain all coordinates with value 9

    for coord_9 in queue:
        trailheads[coord_9] += 1

def main1_impl(tuple_):
    grid = Grid(tuple_, as_int=True)

    n_rows, n_cols = grid.dims()

    trailheads = Counter()

    for row_idx in range(n_rows):
        for col_idx in range(n_cols):
            start = Coordinate(row_idx, col_idx)

            if grid[start] != 0:
                continue

            find_trailhead_unique(start, grid, trailheads)

    total = 0
    for key, value in trailheads.items():
        total += value

    return total

def main2_impl(tuple_):

    grid = Grid(tuple_, as_int=True)

    n_rows, n_cols = grid.dims()

    trailheads = Counter()

    for row_idx in range(n_rows):
        for col_idx in range(n_cols):
            start = Coordinate(row_idx, col_idx)

            if grid[start] != 0:
                continue

            find_trailhead(start, grid, trailheads)

    total = 0
    for key, value in trailheads.items():
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
