from typing import NamedTuple
import math
import itertools
import re
from functools import cache
from collections import deque

def is_in_grid(coords, n_rows, n_cols):

    if coords.row >= 0 and coords.row < n_rows and coords.col >= 0 and coords.col < n_cols:
        return True

    return False

class Coordinate(NamedTuple):
    row: int
    col: int

    def __add__(self, other):
        return Coordinate(self.row + other.row, self.col + other.col)

    def is_in_grid(self, n_rows, n_cols):
        if self.row >= 0 and self.row < n_rows and self.col >= 0 and self.col < n_cols:
            return True

        return False

    def is_on_path(self, grid):
        if grid[self.row][self.col] == '.':
            return True

        return False


DIRECTIONS = {
    Coordinate(0, 1): 'right',
    Coordinate(0, -1): 'left',
    Coordinate(-1, 0): 'up',
    Coordinate(1, 0): 'down'
}

def maina(file):

    grid = []

    with open(file, 'r') as f:
        for line in f:
            grid.append(line.strip())

    start = None

    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == 'S':
                start = Coordinate(row, col)
                grid[row] = grid[row].replace('S', '.')

    n_rows = len(grid)
    n_cols = len(grid[0])

    print(n_rows, n_cols)

    queue = set([start])
    steps = 0
    total_steps = 65 + 131 * 0

    while steps < total_steps:
        new_queue = set()
        for coord in queue:
            for direction in DIRECTIONS.keys():
                new_coord = coord + direction
                if new_coord not in new_queue and new_coord.is_in_grid(n_rows, n_cols) and new_coord.is_on_path(grid):
                    new_queue.add(new_coord)
        queue = new_queue
        steps += 1

    return len(queue)

def mainb(file):

    grid = []

    with open(file, 'r') as f:
        for line in f:
            grid.append(line.strip())

    start = None

    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            if char == 'S':
                start = Coordinate(row, col)
                grid[row] = grid[row].replace('S', '.')

    for i, row in enumerate(grid):
        grid[i] = row * 5

    new_grid = grid.copy()

    for i in range(4):
        new_grid.extend(grid)

    grid = new_grid

    n_rows = len(grid)
    n_cols = len(grid[0])

    print(n_rows, n_cols)

    queue = set([start + Coordinate(262, 262)])
    steps = 0
    total_steps = 65 + 131 * 2

    while steps < total_steps:
        new_queue = set()
        for coord in queue:
            for direction in DIRECTIONS.keys():
                new_coord = coord + direction
                if new_coord not in new_queue and new_coord.is_in_grid(n_rows, n_cols) and new_coord.is_on_path(grid):
                    new_queue.add(new_coord)
        queue = new_queue
        steps += 1

    return len(queue)

if __name__ == '__main__':

    file = './data.txt'
    # print(mainb(file))

    print((26501365 - 65) // 131)

    f0 = 3802
    f1 = 33732
    f2 = 93480

    C = 3802
    A = (f2 - 2*f1 + f0) / 2
    B = f1 - A - C

    print(f'A: {A}, B: {B}, C: {C}')
    print(f'Final answer: {202300**2 * A + 202300 * B + C}')