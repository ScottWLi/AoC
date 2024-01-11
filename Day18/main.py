from typing import NamedTuple
import math
import itertools
import re
from functools import cache
from collections import deque
import heapq
import numpy as np

def process_right(grid, current_row, current_col, steps):

    while steps > 0:
        if current_col == (len(grid[0]) - 1):
            for i, row in enumerate(grid):
                grid[i] = row + '.'
        grid[current_row] = grid[current_row][:current_col+1] + '#' + grid[current_row][current_col+2:]
        current_col += 1

        steps -= 1

    return current_row, current_col

def process_left(grid, current_row, current_col, steps):

    while steps > 0:
        if current_col == 0:
            for i, row in enumerate(grid):
                grid[i] = '.' + row
            current_col = 1
        grid[current_row] = grid[current_row][:current_col - 1] + '#' + grid[current_row][current_col:]
        current_col -= 1

        steps -= 1

    return current_row, current_col

def process_up(grid, current_row, current_col, steps):

    while steps > 0:
        if current_row == 0:
            grid.insert(0, '.'*len(grid[0]))
            current_row = 1
        grid[current_row - 1] = grid[current_row-1][:current_col] + '#' + grid[current_row-1][current_col+1:]
        current_row -= 1

        steps -= 1

    return current_row, current_col

def process_down(grid, current_row, current_col, steps):

    while steps > 0:
        if current_row == (len(grid) - 1):
            grid.append('.'*len(grid[0]))
        grid[current_row + 1] = grid[current_row+1][:current_col] + '#' + grid[current_row+1][current_col+1:]
        current_row += 1

        steps -= 1

    return current_row, current_col

DIRECTION_PROCESSOR = {
    'R': process_right,
    'L': process_left,
    'U': process_up,
    'D': process_down
}

class Step(NamedTuple):
    direction: str
    steps: int

def process_line(grid, current_row, current_col, line):
    direction, steps, colour = tuple(line.split(' '))
    processor = DIRECTION_PROCESSOR[direction]
    current_row, current_col = processor(grid, current_row, current_col, int(steps))
    # print(grid)

    return current_row, current_col

def count_grid(grid):
    total = 0
    for line in grid:
        local = 0
        inside = False
        block = False
        for char in line:
            if char == '#':
                block = True
            else:
                if block:
                    inside = not inside
                    block = False
            if inside or char == '#':
                total += 1
                local += 1
        # print(f'Line {line} has {local} holes!')

    return total

def maina(file):

    grid = ['#']
    history = []

    #current_row and current_col are the coordinates of the last spot where a hole was placed
    current_row = 0
    current_col = 0

    with open(file, 'r') as f:
        for line in f:

            current_row, current_col = process_line(grid, current_row, current_col, line.strip())

    for line in grid:
        print(line)

    total = count_grid(grid)

    return total

class Coordinates(NamedTuple):
    current_row: int
    current_col: int

DIRECTIONS = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}

def PolyArea(x,y):
    return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))

def process_line_new(line, last_corner, bdpts):
    direction, steps, colour = tuple(line.split(' '))
    steps = int(steps)
    direction = DIRECTIONS[direction]
    for i in range(steps):
        bdpts.add(Coordinates(last_corner.current_row + direction[0] * i, last_corner.current_col + direction[1]*i))

    return Coordinates(last_corner.current_row + direction[0] * steps, last_corner.current_col + direction[1]*steps)


def mainaa(file):

    last_corner = Coordinates(0, 0)
    corners = [last_corner]

    xs = [0]
    ys = [0]
    bdpts = set()

    with open(file, 'r') as f:
        for line in f:
            last_corner = process_line_new(line, last_corner, bdpts)
            corners.append(last_corner)
            xs.append(last_corner.current_row)
            ys.append(last_corner.current_col)

    A = PolyArea(xs, ys)
    b = len(bdpts)
    I = A + 1 - b // 2

    return I + b

COLOUR_DIRECTION = {
    '0':'R',
    '1':'D',
    '2':'L',
    '3':'U'
}

def process_line_new_b(line, last_corner):
    direction, steps, colour = tuple(line.strip().split(' '))

    direction = COLOUR_DIRECTION[colour[-2]]
    steps = int(colour[2:-2], 16)

    steps = int(steps)
    direction = DIRECTIONS[direction]


    return Coordinates(last_corner.current_row + direction[0] * steps, last_corner.current_col + direction[1]*steps), steps


def mainb(file):

    last_corner = Coordinates(0, 0)
    corners = [last_corner]

    xs = [0]
    ys = [0]
    b = 0

    with open(file, 'r') as f:
        for line in f:
            last_corner, distance = process_line_new_b(line, last_corner)
            b += distance
            corners.append(last_corner)
            xs.append(last_corner.current_row)
            ys.append(last_corner.current_col)

    A = PolyArea(xs, ys)
    I = A + 1 - b // 2

    return I + b


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))

    # test = ['#######',
    #         '#.....#',
    #         '###...#',
    #         '..#...#',
    #         '..#...#',
    #         '###.###',
    #         '#...#..',
    #         '##..###',
    #         '.#....#',
    #         '.######']
    # print(count_grid(test))