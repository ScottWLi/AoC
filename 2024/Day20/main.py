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
def main1_impl(tuple_):

    grid = Grid(tuple_)

    start = grid.find('S')
    end = grid.find('E')

    directions = [direction.value for direction in DIRECTIONS.simple_directions()]
    distance_from_start = {}

    queue = [
        start
    ]

    distance = 0
    while queue:
        front = queue.pop()
        distance_from_start[front] = distance

        if grid[front] == 'E':
            break

        for direction in directions:
            new_coord = front + direction

            if new_coord not in distance_from_start and new_coord in grid and grid[new_coord] != '#':
                queue.append(new_coord)

        distance += 1

    cheat_spots_saved = {}

    for old_location, old_distance in distance_from_start.items():
        for direction in directions:
            new_location = old_location + (direction * 2)

            if new_location in grid and new_location in distance_from_start and distance_from_start[new_location] < old_distance - 2:
                cheat_spots_saved[old_location + direction] = old_distance - 2 - distance_from_start[new_location]

    count = Counter()
    for key, value in cheat_spots_saved.items():
        count[value] += 1

    total = 0

    for key, value in count.items():
        if key >= 100:
            total += value

    return total


def main2_impl(tuple_):

    grid = Grid(tuple_)

    start = grid.find('S')
    end = grid.find('E')

    directions = [direction.value for direction in DIRECTIONS.simple_directions()]
    distance_from_start = {}

    queue = [
        start
    ]

    distance = 0
    while queue:
        front = queue.pop()
        distance_from_start[front] = distance

        if grid[front] == 'E':
            break

        for direction in directions:
            new_coord = front + direction

            if new_coord not in distance_from_start and new_coord in grid and grid[new_coord] != '#':
                queue.append(new_coord)

        distance += 1

    cheat_spots_saved = {}

    for old_location, old_distance in distance_from_start.items():
        for new_location, new_distance in distance_from_start.items():

            manhattan_distance = new_location.manhattan(old_location)
            if manhattan_distance <= 20 and new_distance < old_distance - manhattan_distance:
                cheat_spots_saved[(old_location, new_location)] = old_distance - manhattan_distance - new_distance

    count = Counter()
    for key, value in cheat_spots_saved.items():
        count[value] += 1

    total = 0

    for key, value in count.items():
        if key >= 100:
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
