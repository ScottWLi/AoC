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

def is_on_edge(coordinate, grid):
    directions = [direction.value for direction in DIRECTIONS.simple_directions()]

    for direction in directions:
        new = coordinate + direction
        if new not in grid or grid[new] != grid[coordinate]:
            return True

    return False

def main1_impl(tuple_):
    grid = Grid(tuple_)

    directions = [direction.value for direction in DIRECTIONS.simple_directions()]

    total = 0

    seen = set()

    n_rows, n_cols = grid.dims()

    for row in range(n_rows):
        for col in range(n_cols):
            if Coordinate(row, col) in seen:
                continue

            queue = [Coordinate(row, col)]
            seen.add(Coordinate(row, col))

            perimeter = 0
            area = 0

            while queue:
                neighbours = 0
                front = queue.pop(0)

                for direction in directions:
                    adjacent = front + direction

                    if adjacent in grid and grid[adjacent] == grid[front]:
                        if adjacent not in seen:
                            queue.append(adjacent)
                            seen.add(adjacent)
                        neighbours += 1

                area += 1
                perimeter += (4 - neighbours)

            total += area * perimeter

    return total

def main2_impl(tuple_):
    grid = Grid(tuple_)

    directions = set(direction.value for direction in DIRECTIONS.simple_directions())

    total = 0

    seen = set()

    n_rows, n_cols = grid.dims()

    for row in range(n_rows):
        for col in range(n_cols):
            if Coordinate(row, col) in seen:
                continue

            queue = [Coordinate(row, col)]
            seen.add(Coordinate(row, col))

            corners = 0
            area = 0

            # put edges to the front of the queue
            # front of the queue now has memory of what added it
            # Sharing a same-edge does NOT add 1 to the perimeter
            #
            # if a piece adds a N

            while queue:
                front = queue.pop(0)
                element_edges = set()

                # Check the edges that the current element has
                for direction in directions:
                    adjacent = front + direction

                    if adjacent not in grid or grid[adjacent] != grid[front]:
                        element_edges.add(direction)

                # This is a new edge
                # Corner checks

                if DIRECTIONS.UP.value in element_edges and DIRECTIONS.RIGHT.value in element_edges:
                    corners += 1
                if DIRECTIONS.UP.value in element_edges and DIRECTIONS.LEFT.value in element_edges:
                    corners += 1
                if DIRECTIONS.DOWN.value in element_edges and DIRECTIONS.RIGHT.value in element_edges:
                    corners += 1
                if DIRECTIONS.DOWN.value in element_edges and DIRECTIONS.LEFT.value in element_edges:
                    corners += 1

                if DIRECTIONS.UP.value not in element_edges and DIRECTIONS.RIGHT.value not in element_edges:
                    up_right = front + DIRECTIONS.UP_RIGHT.value
                    if grid[up_right] != grid[front]:
                        corners += 1
                if DIRECTIONS.UP.value not in element_edges and DIRECTIONS.LEFT.value not in element_edges:
                    up_left = front + DIRECTIONS.UP_LEFT.value
                    if grid[up_left] != grid[front]:
                        corners += 1
                if DIRECTIONS.DOWN.value not in element_edges and DIRECTIONS.RIGHT.value not in element_edges:
                    down_right = front + DIRECTIONS.DOWN_RIGHT.value
                    if grid[down_right] != grid[front] :
                        corners += 1
                if DIRECTIONS.DOWN.value not in element_edges and DIRECTIONS.LEFT.value not in element_edges:
                    down_left = front + DIRECTIONS.DOWN_LEFT.value
                    if grid[down_left] != grid[front] :
                        corners += 1


                # Check adjacent elements in the same group
                for direction in directions.difference(element_edges):
                    adjacent = front + direction
                    if adjacent not in grid:
                        continue

                    if adjacent not in seen:
                        queue.append(adjacent)
                        seen.add(adjacent)

                area += 1

            print(f'A region of {grid[Coordinate(row, col)]} plants with price {area} * {corners} = {area * corners}')
            total += area * corners

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
