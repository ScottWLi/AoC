from typing import NamedTuple
import math
import itertools
import re
from functools import cache
from collections import deque

PATTERN = r"\s*(-*\d+)"

DIRECTIONS = {
    (0, 1): 'right',
    (0, -1): 'left',
    (-1, 0): 'up',
    (1, 0): 'down'
}

RIGHT_DIRECTION = {
    '.': [(0, 1)],
    '-': [(0, 1)],
    '|': [(-1, 0), (1, 0)],
    '\\': [(1, 0)],
    '/': [(-1, 0)]
}

LEFT_DIRECTION = {
    '.': [(0, -1)],
    '-': [(0, -1)],
    '|': [(-1, 0), (1, 0)],
    '\\': [(-1, 0)],
    '/': [(1, 0)]
}

UP_DIRECTION = {
    '.': [(-1, 0)],
    '-': [(0, 1), (0, -1)],
    '|': [(-1, 0)],
    '\\': [(0, -1)],
    '/': [(0, 1)]
}

DOWN_DIRECTION = {
    '.': [(1, 0)],
    '-': [(0, 1), (0, -1)],
    '|': [(1, 0)],
    '\\': [(0, 1)],
    '/': [(0, -1)]
}

DIRECTION_LOOKUP = {
    'right':RIGHT_DIRECTION,
    'up': UP_DIRECTION,
    'down': DOWN_DIRECTION,
    'left': LEFT_DIRECTION
}

class Beam(NamedTuple):
    coords: tuple
    direction: str

def is_in_grid(coords, n_rows, n_cols):

    if coords[0] >= 0 and coords[0] < n_rows and coords[1] >= 0 and coords[1] < n_cols:
        return True

    return False

def maina(file):

    grid = []

    with open(file, 'r') as f:
        for line in f:
            grid.append(line.strip())

    start_beam = Beam((0, 0), 'right')


    return coords_energised(grid, start_beam)



def coords_energised(grid, start_beam):

    m = len(grid)
    n = len(grid[0])

    queue = deque([start_beam])
    seen = set([start_beam])

    while queue:
        front = queue.popleft()
        coords, direction = front.coords, front.direction
        symbol = grid[coords[0]][coords[1]]

        direction_list = DIRECTION_LOOKUP[direction][symbol]

        for drow, dcol in direction_list:
            new_coords = (coords[0] + drow, coords[1] + dcol)
            new_beam = Beam(new_coords, DIRECTIONS[(drow, dcol)])
            if is_in_grid(new_coords, m, n) and new_beam not in seen:
                queue.append(new_beam)
                seen.add(new_beam)

    coords_seen = set()

    for item in seen:
        if item.coords not in coords_seen:
            coords_seen.add(item.coords)

    return len(coords_seen)

def mainb(file):

    grid = []

    with open(file, 'r') as f:
        for line in f:
            grid.append(line.strip())

    maximum = 0

    m = len(grid)
    n = len(grid[0])

    for i in range(m):
        start_beam = Beam((i, 0), 'right')
        maximum = max(maximum, coords_energised(grid, start_beam))
        start_beam = Beam((i, n-1), 'left')
        maximum = max(maximum, coords_energised(grid, start_beam))

    for j in range(n):
        start_beam = Beam((0, j), 'down')
        maximum = max(maximum, coords_energised(grid, start_beam))
        start_beam = Beam((m-1, j), 'up')
        maximum = max(maximum, coords_energised(grid, start_beam))

    return maximum


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))