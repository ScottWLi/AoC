import posix
from ast import literal_eval
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

def do_bfs(start, end, grid):
    seen = {start}
    queue = [start]
    steps = 0

    simple_directions = [direction.value for direction in DIRECTIONS.simple_directions()]

    while queue :
        new_queue = []
        for front in queue :

            if front == end :
                return steps

            for direction in simple_directions :
                new_coord = front + direction

                if new_coord in grid and grid[new_coord] != '#' and new_coord not in seen :
                    new_queue.append(new_coord)
                    seen.add(new_coord)
                    grid[new_coord] = 'O'

        queue = new_queue
        steps += 1

    return -1

def main1_impl(tuple_):

    len = 71
    bytes = 1024

    new_grid = [['.'] * len for _ in range(len)]

    grid = Grid(new_grid)

    for i in range(bytes):
        x, y = tuple_[i].split(',')
        coordinate = Coordinate(int(y), int(x))
        grid[coordinate] = '#'

    start = Coordinate(0,0)
    end = Coordinate(len-1, len-1)

    do_bfs(start, end, grid)
    return do_bfs(start, end, grid)


def main2_impl(tuple_):

    len_ = 71
    bytes = 1024

    new_grid = [['.'] * len_ for _ in range(len_)]

    grid = Grid(new_grid)

    for i in range(bytes):
        x, y = tuple_[i].split(',')
        coordinate = Coordinate(int(y), int(x))
        grid[coordinate] = '#'

    start = Coordinate(0,0)
    end = Coordinate(len_-1, len_-1)

    for i in range(bytes+1, len(tuple_)):
        x, y = tuple_[i].split(',')
        coordinate = Coordinate(int(y), int(x))
        grid[coordinate] = '#'

        do_bfs(start, end, grid)

        if do_bfs(start, end, grid) == -1:
            return ','.join((x, y))

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
