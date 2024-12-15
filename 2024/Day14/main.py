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

def parse_input(input):

    ret = []
    P = re.compile(r"p=([0-9]+,[0-9]+)")
    V = re.compile(r"v=(-?[0-9]+,-?[0-9]+)")

    for row in input:

        p = P.search(row)
        v = V.search(row)

        p_col, p_row = p.group(1).split(',')
        v_col, v_row = v.group(1).split(',')

        p_coord = Coordinate(int(p_row), int(p_col))
        v_coord = Coordinate(int(v_row), int(v_col))

        ret.append((p_coord, v_coord))

    return ret


def main1_impl(tuple_):

    robots = parse_input(tuple_)
    height = 103
    width = 101

    seconds = 100

    grid = Grid([[0] * width for _ in range(height)])

    for initial_position, velocity in robots:
        raw_final_position = initial_position + velocity * seconds

        final_position = Coordinate(raw_final_position.row % height, raw_final_position.column % width)
        grid[final_position] += 1


    middle = Coordinate(height // 2, width // 2)

    #TL
    TL = 0
    for row in range(middle.row):
        for col in range(middle.column):
            current = Coordinate(row, col)
            TL += grid[current]

    #TR
    TR = 0
    for row in range(middle.row):
        for col in range(middle.column + 1, width):
            current = Coordinate(row, col)
            TR += grid[current]

    #BL
    BL = 0
    for row in range(middle.row + 1, height):
        for col in range(middle.column):
            current = Coordinate(row, col)
            BL += grid[current]

    #BR
    BR = 0
    for row in range(middle.row + 1, height):
        for col in range(middle.column + 1, width):
            current = Coordinate(row, col)
            BR += grid[current]

    return BR * TR * BL * TL

def main2_impl(tuple_):

    robots = parse_input(tuple_)
    height = 103
    width = 101

    for idx in range(101):

        seconds = 19 + 103 * idx

        grid = Grid([[0] * width for _ in range(height)])

        for initial_position, velocity in robots:
            raw_final_position = initial_position + velocity * seconds

            final_position = Coordinate(raw_final_position.row % height, raw_final_position.column % width)
            grid[final_position] += 1

        for row_idx, row in enumerate(grid.grid):
            for col_idx, char in enumerate(row):
                if not char:
                    grid[Coordinate(row_idx, col_idx)] = ' '

        print('---------')
        print(seconds)
        print('---------')
        print(grid)


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
