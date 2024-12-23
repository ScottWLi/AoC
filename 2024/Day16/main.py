import posix
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


def main1_impl(tuple_):
    grid = Grid(tuple_)
    start = grid.find('S')

    directions = {direction.value for direction in DIRECTIONS.simple_directions()}

    # Queue is a heapq containing tuples of the form (cost, location, direction)
    queue = []
    heapq.heappush(queue, (0, start, DIRECTIONS.RIGHT.value))
    seen = {start}

    while heapq:
        cost, location, direction = heapq.heappop(queue)
        if grid[location] == 'E':
            return cost

        new_location = location + direction
        if new_location not in seen and grid[new_location] != '#':
            heapq.heappush(queue, (cost + 1, new_location, direction))
            seen.add(new_location)

        adjacent_directions = directions.copy()

        adjacent_directions.remove(-1 * direction)
        adjacent_directions.remove(direction)

        for adjacent_direction in adjacent_directions:
            new_location = location + adjacent_direction
            if new_location not in seen and grid[new_location] != '#':
                heapq.heappush(queue, (cost + 1001, new_location, adjacent_direction))
                seen.add(new_location)

    raise RuntimeError(f"Unexpected failure of search algorithm for grid \n {grid}")

def main2_impl(tuple_):
    grid = Grid(tuple_)
    start = grid.find('S')

    directions = {direction.value for direction in DIRECTIONS.simple_directions()}

    # Queue is a heapq containing tuples of the form (cost, location, direction)
    queue = []
    heapq.heappush(queue, (0, start, DIRECTIONS.RIGHT.value, {start}))

    # Need some notion of history
    # Turn seen into a dictionary that maps location: (cost, set(historical path))
    # If we get to a point in seen and its cost is 1001 higher (i.e. we turned earlier but its equivalent)
    # Then we can add our historical path to its historical path

    # Reverse loop on the path:
    # Go through each element on the historical path
    # Add it to a set. Add it to the historical paths to check
    # history includes itself
    seen = {start: [0, set(start)]}

    while heapq:
        cost, location, direction, history = heapq.heappop(queue)
        if grid[location] == 'E':
            seen[location] = [cost, history]
            break

        new_location = location + direction
        if new_location in seen:
            # print(f'Location: {location}, looking {direction}, with cost {cost}, best_cost {seen[new_location][0]}')
            # We meet the most-efficient path before it has turned or we both find the optimal path at the same time
            if ((cost - 999) == seen[new_location][0] and grid[new_location + direction] != '#') or (cost + 1) == seen[new_location][0]:
                # print('ever here?')
                seen[new_location][1].update(history)
        if new_location not in seen and grid[new_location] != '#':
            new_history = history.copy()
            new_history.add(new_location)
            heapq.heappush(queue, (cost + 1, new_location, direction, new_history))

        adjacent_directions = directions.copy()

        adjacent_directions.remove(-1 * direction)
        adjacent_directions.remove(direction)

        for adjacent_direction in adjacent_directions:
            new_location = location + adjacent_direction
            if new_location not in seen and grid[new_location] != '#':
                new_history = history.copy()
                new_history.add(new_location)
                heapq.heappush(queue, (cost + 1001, new_location, adjacent_direction, new_history))

        seen[location] = [cost, history]

    best_seats = history.copy()
    best_seats.add(location)
    backwards_queue = list(best_seats.copy())

    while backwards_queue:
        all_paths_to_front = seen[backwards_queue.pop()][1]

        difference = all_paths_to_front.difference(best_seats)
        for item in difference:
            best_seats.add(item)
            backwards_queue.append(item)

    test = list(best_seats)
    test.sort(key = lambda x: (x.row, x.column))

    for coordinate in test:
        grid[coordinate] = 'O'
    print(grid)

    return len(best_seats)

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
