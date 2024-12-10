from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS, GridPointer
from collections import Counter
from functools import cmp_to_key
import re

def main1_impl(tuple_):
    grid = Grid(tuple_)

    start = grid.find('^')
    walker = GridPointer(start, DIRECTIONS.UP)

    while walker.location in grid:
        in_front = walker.in_front_of()

        if in_front in grid and grid[in_front] == '#':
            walker = walker.turn_right()
        else:
            grid[walker.location] = 'X'
            walker = walker.walk()

    return grid.count('X')


def main2_impl(tuple_):
    grid = Grid(tuple_)

    start = grid.find('^')
    walker = GridPointer(start, DIRECTIONS.UP)

    possible_locations = []
    seen = set(start)

    while walker.location in grid:
        in_front = walker.in_front_of()

        if in_front in grid and grid[in_front] == '#':
            walker = walker.turn_right()
        else:
            if walker.in_front_of() not in seen:
                possible_locations.append(walker)
                seen.add(walker.in_front_of())
            walker = walker.walk()

    total = 0

    for extra in possible_locations:
        new_grid = Grid(tuple_)
        if extra.in_front_of() not in grid:
            continue
        new_grid[extra.in_front_of()] = '#'

        walker = extra
        seen_locations = set((GridPointer(start, DIRECTIONS.UP),))

        while walker.location in new_grid:
            in_front = walker.in_front_of()

            if in_front in new_grid and new_grid[in_front] == '#':
                walker = walker.turn_right()
            else:
                if walker in seen_locations:
                    total += 1
                    break
                seen_locations.add(walker)
                walker = walker.walk()

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
