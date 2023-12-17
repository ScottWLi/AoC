from typing import NamedTuple
import math
import itertools
import re
from functools import cache

PATTERN = r"\s*(-*\d+)"

def weight_of_n_from_row(n, row):
    if n == 1:
        return row
    elif n == 0:
        return 0

    return row + weight_of_n_from_row(n-1, row-1)

def maina(file):
    total = 0

    grid = []
    with open(file, 'r') as f:
        for line in f:
                grid.append(line.strip())

    m = len(grid)
    n = len(grid[0])

    for j in range(n):
        # print(f'Column {j}')
        n_rocks = 0
        ceil_index = 0

        for i, row in enumerate(grid):
            if row[j] == 'O':
                n_rocks += 1
            elif row[j] == '#':
                value = weight_of_n_from_row(n_rocks, m - ceil_index)
                # print(f'Adding weight of {value}')
                total += value
                ceil_index = i + 1
                n_rocks = 0
        if n_rocks > 0:
            value = weight_of_n_from_row(n_rocks, m - ceil_index)
            # print(f'Adding weight of {value}')
            total += value

    return total

def push_up(grid):
    n = len(grid[0])

    for j in range(n):
        n_rocks = 0
        ceil_index = 0

        for i, row in enumerate(grid):
            if row[j] == 'O':
                n_rocks += 1
                grid[i] = row[:j] + '.' + row[j+1:]
            elif row[j] == '#':
                counter = 0
                while counter < n_rocks:
                    grid[ceil_index + counter] = grid[ceil_index + counter][:j] + 'O' + grid[ceil_index + counter][j+1:]
                    counter += 1
                ceil_index = i + 1
                n_rocks = 0

        if n_rocks > 0:
            counter = 0
            while counter < n_rocks:
                grid[ceil_index + counter] = grid[ceil_index + counter][:j] + 'O' + grid[ceil_index + counter][j + 1:]
                counter += 1

    # print('Push up:')
    # print_grid(grid)

    return grid

def push_left(grid):

    m = len(grid)
    n = len(grid[0])

    for i, row in enumerate(grid):
        n_rocks = 0
        ceil_index = 0
        # print(f'Old row: {row}')
        for j, char in enumerate(row):
            if char == 'O':
                n_rocks += 1
                grid[i] = grid[i][:j] + '.' + grid[i][j+1:]
            elif char == '#':
                grid[i] = grid[i][:ceil_index] + 'O' * n_rocks + grid[i][ceil_index + n_rocks:]
                ceil_index = j + 1
                n_rocks = 0

        if n_rocks > 0:
            grid[i] = grid[i][:ceil_index] + 'O' * n_rocks + grid[i][ceil_index + n_rocks:]
        # print(f'New row: {grid[i]}')

    # print('Push left:')
    # print_grid(grid)


    return grid

def push_right(grid):
    m = len(grid)
    n = len(grid[0])

    for i, row in enumerate(grid):
        n_rocks = 0

        for j, char in enumerate(row):
            if char == 'O':
                n_rocks += 1
                grid[i] = grid[i][:j] + '.' + grid[i][j + 1:]
            elif char == '#':
                grid[i] = grid[i][:j-n_rocks] + 'O' * n_rocks + grid[i][j:]
                n_rocks = 0

        if n_rocks > 0:
            grid[i] = grid[i][:n-n_rocks] + 'O' * n_rocks

    # print('Push right:')
    # print_grid(grid)

    return grid

def push_down(grid):
    n = len(grid[0])
    m = len(grid)

    for j in range(n):
        n_rocks = 0

        for i, row in enumerate(grid):
            if row[j] == 'O':
                n_rocks += 1
                grid[i] = grid[i][:j] + '.' + grid[i][j+1:]
            elif row[j] == '#':
                counter = 0
                while counter < n_rocks:
                    grid[i - 1 - counter] = grid[i - 1 - counter][:j] + 'O' + grid[i - 1 - counter][j+1:]
                    counter += 1
                ceil_index = i + 1
                n_rocks = 0

        if n_rocks > 0:
            counter = 0
            while counter < n_rocks:
                grid[m - 1 - counter] = grid[m - 1 - counter][:j] + 'O' + grid[m - 1 - counter][j + 1:]
                counter += 1

    # print('Push down:')
    # print_grid(grid)

    return grid

def cycle_grid(grid):
    grid = push_up(grid)
    grid = push_left(grid)
    grid = push_down(grid)
    grid = push_right(grid)

    return grid

def print_grid(grid):
    for line in grid:
        print(line)

    print('\n')

def count_weight(grid):
    total = 0
    m = len(grid)

    for i, row in enumerate(grid):
        for char in row:
            if char == 'O':
                total += m - i

    return total

def check_grids_are_equal(grid, prev_grid):
    for i in range(len(grid)):
        if grid[i] != prev_grid[i]:
            return False

    return True

def mainaa(file):
    total = 0

    grid = []
    with open(file, 'r') as f:
        for line in f:
            grid.append(line.strip())

    grid = push_up(grid)

    return count_weight(grid)

def mainb(file):
    total = 0

    grid = []
    with open(file, 'r') as f:
        for line in f:
            grid.append(line.strip())

    # print_grid(grid)
    first_grid = grid.copy()

    for i in range(1000):
        prev_grid = grid.copy()
        grid = cycle_grid(grid)
        # print(f'Cycled {i + 1} times:')
        # print(f'Equal to previous grid: {check_grids_are_equal(grid, prev_grid)}')
        # print_grid(grid)

    grid_check = grid.copy()
    for i in range(100):
        if (i + 1000) % 35 == 20:
            return count_weight(grid)
        grid = cycle_grid(grid)

        if check_grids_are_equal(grid, grid_check):
            print(i)


    # print_grid(first_grid)
    # print_grid(grid)

    return None


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))