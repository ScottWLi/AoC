from typing import NamedTuple
import math
import itertools
import re
from functools import cache
from collections import deque
import heapq

DIRECTIONS = {
    (0, 1): 'right',
    (0, -1): 'left',
    (-1, 0): 'up',
    (1, 0): 'down'
}

OPPOSITE = {
    'right': 'left',
    'left': 'right',
    'up': 'down',
    'down': 'up',
    'none':'none'
}

class Node(NamedTuple):
    coords: tuple
    direction: str
    steps: int

def is_in_boundary(coords, n_rows, n_cols):
    if coords[0] >= 0 and coords[0] < n_rows and coords[1] >= 0 and coords[1] < n_cols:
        return True

    return False

def get_neighbours(node:Node, n_rows, n_cols):

    neighbour_list = []

    for (drow, dcol), key in DIRECTIONS.items():
        coords = node.coords[0] + drow, node.coords[1] + dcol
        if is_in_boundary(coords, n_rows, n_cols) and key != OPPOSITE[node.direction]:
            if key == node.direction:
                if node.steps < 3:
                    neighbour_list.append(Node(coords, key, node.steps+1))
            else:
                neighbour_list.append(Node(coords, key, 1))

    # print(f'{node} has neighboburs {neighbour_list}')

    return neighbour_list

def maina(file):

    grid = []

    with open(file, 'r') as f:
        for line in f:
            line_ints = [int(char) for char in line.strip()]
            grid.append(line_ints)

    m = len(grid)
    n = len(grid[0])

    distances = {Node((0, 0), 'none', 0): 0}

    pq = [(0, Node((0, 0), 'none', 0))]

    while pq:

        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        node_neighbours = get_neighbours(current_node, m, n)

        for neighbour in node_neighbours:
            coords = neighbour.coords
            distance = current_distance + grid[coords[0]][coords[1]]

            # Only consider this new path if it's better than any path we've
            # already found.
            if neighbour not in distances or distance < distances[neighbour]:
                distances[neighbour] = distance
                heapq.heappush(pq, (distance, neighbour))

    minimum = None
    debug_coords = (12, 12)

    for key, value in distances.items():
        if key.coords == debug_coords:
            print(key, value)
        if key.coords == (m-1, n-1):
            if not minimum:
                minimum = value
            else:
                minimum = min(minimum, value)

    return minimum

def get_neighbours_b(node:Node, n_rows, n_cols):

    neighbour_list = []

    for (drow, dcol), key in DIRECTIONS.items():
        coords = node.coords[0] + drow, node.coords[1] + dcol
        if is_in_boundary(coords, n_rows, n_cols) and key != OPPOSITE[node.direction]:
            if key == node.direction:
                if node.steps < 10:
                    neighbour_list.append(Node(coords, key, node.steps+1))
            else:
                if node.steps > 3 or node.direction == 'none':
                    neighbour_list.append(Node(coords, key, 1))

    # print(f'{node} has neighboburs {neighbour_list}')

    return neighbour_list

def mainb(file):

    grid = []

    with open(file, 'r') as f:
        for line in f:
            line_ints = [int(char) for char in line.strip()]
            grid.append(line_ints)

    m = len(grid)
    n = len(grid[0])

    distances = {Node((0, 0), 'none', 0): 0}

    pq = [(0, Node((0, 0), 'none', 0))]

    while pq:

        current_distance, current_node = heapq.heappop(pq)

        if current_distance > distances[current_node]:
            continue

        node_neighbours = get_neighbours_b(current_node, m, n)

        for neighbour in node_neighbours:
            coords = neighbour.coords
            distance = current_distance + grid[coords[0]][coords[1]]

            # Only consider this new path if it's better than any path we've
            # already found.
            if neighbour not in distances or distance < distances[neighbour]:
                distances[neighbour] = distance
                heapq.heappush(pq, (distance, neighbour))

    minimum = None
    debug_coords = (12, 12)

    for key, value in distances.items():
        # if key.coords == debug_coords:
        #     print(key, value)
        if key.coords == (m-1, n-1):
            if key.steps >= 4:
                if not minimum:
                    minimum = value
                else:
                    minimum = min(minimum, value)

    return minimum


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))