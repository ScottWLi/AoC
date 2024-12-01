from typing import NamedTuple
import math
import itertools
import re
from functools import cache

PATTERN = r"\s*(-*\d+)"

def is_vert_reflection(grid, column):
    """column is such that the axis of reflection has column columns to the left"""
    m = len(grid)
    n = len(grid[0])
    index = 0

    while (column - index - 1) >= 0 and (column + index < n):
        for row in grid:
            if row[column - index - 1] != row[column + index]:
                return False
        index += 1

    return True

def is_horiz_reflection(grid, row):
    """row is such that the axis of relection has row rows above it"""
    m = len(grid)
    n = len(grid[0])
    index = 0

    while (row - index - 1) >= 0 and (row + index) < m:
        if grid[row-index-1] != grid[row + index]:
            return False
        index += 1

    return True

def calculate_problem_number(grid):
    m = len(grid)
    n = len(grid[0])

    for col in range(1, n):
        if is_vert_reflection(grid, col):
            # print(f'Vertical reflection at {col}')
            return col, 'vert'
    for row in range(1, m):
        if is_horiz_reflection(grid, row):
            # print(f'Horizontal reflection at {row}')
            return row, 'horiz'


    return -1

def calculate_problem_number_exclusion(grid, value, type):
    m = len(grid)
    n = len(grid[0])

    for col in range(1, n):
        if type == 'vert' and col == value:
            continue
        if is_vert_reflection(grid, col):
            print(f'Vertical reflection at {col}')
            return col, 'vert'
    for row in range(1, m):
        if type == 'horiz' and row == value:
            continue
        if is_horiz_reflection(grid, row):
            print(f'Horizontal reflection at {row}')
            return row, 'horiz'


    return -1, 'broken'

def maina(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    total = 0

    grid = []
    with open(file, 'r') as f:
        for line in f:
            if line == '\n':
                print(grid)
                value, type = calculate_problem_number(grid)

                if type == 'vert':
                    total += value
                else:
                    total += value * 100

                grid = []

            else:
                grid.append(line.strip())

    return total

def mainb(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    total = 0

    grid = []
    with open(file, 'r') as f:
        for line in f:
            if line == '\n':
                print(grid)
                m = len(grid)
                n = len(grid[0])

                value, type = calculate_problem_number(grid)

                double_break = False

                for i in range(m):
                    for j in range(n):
                        grid_copy = grid.copy()
                        if grid_copy[i][j] == '#':
                            grid_copy[i] = grid_copy[i][:j] + '.' + grid_copy[i][j+1:]
                        else:
                            grid_copy[i] = grid_copy[i][:j] + '#' + grid_copy[i][j+1:]
                        # print(grid_copy)
                        swap_value, swap_type = calculate_problem_number_exclusion(grid_copy, value, type)
                        # print(swap_value, swap_type)
                        if swap_value != -1:
                            print(f'Swap char at {i, j}')
                            if swap_type == 'vert':
                                total += swap_value
                            elif swap_type == 'horiz':
                                total += swap_value * 100
                            double_break = True
                            break
                    if double_break:
                        break

                grid = []

            else:
                grid.append(line.strip())

    return total



if __name__ == '__main__':

    file = './data.txt'

    print(mainb(file))
