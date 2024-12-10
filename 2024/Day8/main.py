from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS, GridPointer
from collections import Counter
from functools import cmp_to_key
from itertools import product, combinations
import re
import math

def main1_impl(tuple_):

    grid = Grid(tuple_)
    n_rows, n_cols = grid.dims()

    antennas = dict()

    for row_i in range(n_rows):
        for col_i in range(n_cols):
            coord = Coordinate(row_i, col_i)
            grid_val: str = grid[coord]
            if grid_val.isalnum():
                if grid_val in antennas:
                    antennas[grid_val].append(coord)
                else:
                    antennas[grid_val] = [coord]

    antinodes = set()

    for values in antennas.values():
        combos = combinations(values, 2)

        for combo in combos:
            difference = combo[0] - combo[1]

            an_1 = combo[0] + difference
            an_2 = combo[1] - difference

            if an_1 in grid:
                antinodes.add(an_1)
            if an_2 in grid:
                antinodes.add(an_2)

    return len(antinodes)

def main2_impl(tuple_):

    grid = Grid(tuple_)
    n_rows, n_cols = grid.dims()

    antennas = dict()

    for row_i in range(n_rows):
        for col_i in range(n_cols):
            coord = Coordinate(row_i, col_i)
            grid_val: str = grid[coord]
            if grid_val.isalnum():
                if grid_val in antennas:
                    antennas[grid_val].append(coord)
                else:
                    antennas[grid_val] = [coord]

    antinodes = set()

    for values in antennas.values():
        combos = combinations(values, 2)

        for combo in combos:
            difference = combo[0] - combo[1]

            gcd = math.gcd(difference.row, difference.column)

            min_difference = difference / gcd

            idx = 0
            while True:
                an_1 = combo[0] + (min_difference * idx)
                an_2 = combo[1] - (min_difference * idx)

                if an_1 not in grid and an_2 not in grid:
                    break

                if an_1 in grid :
                    antinodes.add(an_1)
                if an_2 in grid :
                    antinodes.add(an_2)

                idx += 1

    return len(antinodes)

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
