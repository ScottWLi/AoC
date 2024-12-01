from typing import NamedTuple
import math
import itertools
import re


PATTERN = r"\s*(-*\d+)"


def add_row_to_grid(grid, position):
    """Inserts a row at position"""
    n = len(grid[0])
    new_row = '.' * n

    grid.insert(position, new_row)

def add_column_to_grid(grid, position):
    m = len(grid[0])

    for i, row in enumerate(grid):
        grid[i] = row[:position] + '.' + row[position:]

def find_empty_rows(grid):

    indices = []

    for i, row in enumerate(grid):
        indices.append(i)
        for char in row:
            if char != '.':
                indices.pop()
                break

    return indices

def find_empty_columns(grid):

    indices = []
    n = len(grid[0])

    for j in range(n):
        indices.append(j)
        for row in grid:
            if row[j] != '.':
                indices.pop()
                break

    return indices

def L1_distance(point1, point2):
    return abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])

def row_between(row, point1, point2):
    if row > min(point1[0], point2[0]) and row < max(point1[0], point2[0]):
        return True

    return False

def col_between(col, point1, point2):
    if col > min(point1[1], point2[1]) and col < max(point1[1], point2[1]):
        return True

    return False

def maina(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    sum = 0
    grid = []

    with open(file, 'r') as f:

        for line in f:

            grid.append(line.strip())

    empty_rows = find_empty_rows(grid)
    empty_cols = find_empty_columns(grid)

    offset = 0
    for row_index in empty_rows:
        add_row_to_grid(grid, row_index + offset)
        offset += 1

    offset = 0
    for col_index in empty_cols:
        add_column_to_grid(grid, col_index + offset)
        offset += 1

    print(grid)

    galaxies = []

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == '#':
                galaxies.append((i, j))

    n = len(galaxies)

    for i in range(n):
        for j in range(i + 1, n):
            sum += L1_distance(galaxies[i], galaxies[j])
            # print(f'Distance between {galaxies[i]} and {galaxies[j]}: {L1_distance(galaxies[i], galaxies[j])}')

    return sum

def mainb(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    sum = 0
    grid = []

    with open(file, 'r') as f:

        for line in f:

            grid.append(line.strip())

    empty_rows = find_empty_rows(grid)
    empty_cols = find_empty_columns(grid)

    galaxies = []

    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            if char == '#':
                galaxies.append((i, j))

    n = len(galaxies)

    for i in range(n):
        for j in range(i + 1, n):
            distance = 999999
            additional_distance = 0
            normal_distance = L1_distance(galaxies[i], galaxies[j])
            for row in empty_rows:
                if row_between(row, galaxies[i], galaxies[j]):
                    additional_distance += distance

            for col in empty_cols:
                if col_between(col, galaxies[i], galaxies[j]):
                    additional_distance += distance

            sum += normal_distance + additional_distance

    return sum

if __name__ == '__main__':

    file = './data.txt'

    print(mainb(file))