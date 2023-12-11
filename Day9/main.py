from typing import NamedTuple
import math
import itertools
import re
from collections import deque

LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

PATTERN = r"\s*(-*\d+)"
RIGHT_CONNECTORS = set(['-', 'J', '7'])
LEFT_CONNECTORS = set(['-', 'L', 'F'])
TOP_CONNECTORS = set(['|', '7', 'F'])
BOT_CONNECTORS = set(['|', 'J', 'L'])

CONNECTORS = {
    LEFT: LEFT_CONNECTORS,
    RIGHT: RIGHT_CONNECTORS,
    UP: TOP_CONNECTORS,
    DOWN: BOT_CONNECTORS
}

DIRECTIONS = {
    '|': [UP, DOWN],
    '-': [LEFT, RIGHT],
    'L': [UP, RIGHT],
    'J': [UP, LEFT],
    '7': [LEFT, DOWN],
    'F': [RIGHT, DOWN],
}

ANGLES = {
    'none': 0,
    'right': -90,
    'left': 90
}

# AC_LOOPCHECK = {
#     DOWN: [(-1, 1), (0, 1), (1, 1)],
#     LEFT: [(1,-1), (1, 0), (1, 1)],
#     UP: [(-1, -1), (0, -1), (1, -1)],
#     RIGHT: [(-1, -1), (-1, 0), (-1, 1)]
# }
#
# C_LOOPCHECK = {
#     UP: [(-1, 1), (0, 1), (1, 1)],
#     RIGHT: [(1,-1), (1, 0), (1, 1)],
#     DOWN: [(-1, -1), (0, -1), (1, -1)],
#     LEFT: [(-1, -1), (-1, 0), (-1, 1)]
# }

AC_LOOPCHECK = {
    DOWN: [(0, 1)],
    LEFT: [(1, 0)],
    UP: [(0, -1)],
    RIGHT: [(-1, 0)]
}

C_LOOPCHECK = {
    UP: [(0, 1)],
    RIGHT: [(1, 0)],
    DOWN: [(0, -1)],
    LEFT: [(-1, 0)]
}

def maina(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid

    grid = []

    with open(file, 'r') as f:

        for line in f:

            grid.append(list(line.strip()))

    n_rows = len(grid)
    n_cols = len(grid[0])

    for row_i, row in enumerate(grid):
        for col_j, col in enumerate(row):
            if grid[row_i][col_j] == 'S':
                S_row, S_col = row_i, col_j
                break

    directions = [(0, -1), (0, 1), (-1, 0), (1,0)]

    queue = []
    seen = set([(S_row, S_col)])

    for drow, dcol in directions:
        nrow, ncol = S_row + drow, S_col + dcol

        if nrow >= 0 and nrow < n_rows and ncol >= 0 and ncol < n_cols:
            if grid[nrow][ncol] in CONNECTORS[(drow, dcol)]:
                queue.append((nrow, ncol))
                seen.add((nrow, ncol))

    distance = 1

    while queue:
        print(queue)
        new_queue = []
        for current in queue:
            current_letter = grid[current[0]][current[1]]
            directions = DIRECTIONS[current_letter]

            for drow, dcol in directions:
                nrow, ncol = current[0] + drow, current[1] + dcol
                if (nrow, ncol) not in seen:
                    print((nrow, ncol))
                    new_queue.append((nrow, ncol))
                    seen.add((nrow, ncol))

        queue = new_queue
        distance += 1
        print(distance)

    print("Finished")

    return distance - 1

def mainb(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid

    grid = []

    with open(file, 'r') as f:

        for line in f:

            grid.append(list(line.strip()))

    n_rows = len(grid)
    n_cols = len(grid[0])

    for row_i, row in enumerate(grid):
        for col_j, col in enumerate(row):
            if grid[row_i][col_j] == 'S':
                S_row, S_col = row_i, col_j
                break

    directions = [(0, -1), (0, 1), (-1, 0), (1,0)]

    current = None
    seen = [(S_row, S_col)]
    queue = []

    for drow, dcol in directions:
        nrow, ncol = S_row + drow, S_col + dcol

        if nrow >= 0 and nrow < n_rows and ncol >= 0 and ncol < n_cols and grid[nrow][ncol] in CONNECTORS[(drow, dcol)]:
            queue.append((nrow, ncol))
            seen.append((nrow, ncol))


    current = queue[0]
    end = queue[1]
    seen.remove(end)

    print(current, end)
    counter = 0

    while current != end:
        # print(f'In main loop considering {current}')
        current_letter = grid[current[0]][current[1]]
        directions = DIRECTIONS[current_letter]

        for drow, dcol in directions:
            nrow, ncol = current[0] + drow, current[1] + dcol
            if (nrow, ncol) not in seen:
                # print(f'{current_letter} at ({current[0], current[1]}) gives me ({nrow},{ncol})')
                current = (nrow, ncol)
                seen.append((nrow, ncol))
                break

    seen.append((S_row, S_col))
    seen.append(seen[1])

    print(current, end)
    print(seen)

    angle = 0

    for i in range(1, len(seen) - 1):
        before = seen[i-1]
        mid = seen[i]
        after = seen[i+1]

        before_turn = (mid[0] - before[0], mid[1] - before[1])
        after_turn = (after[0] - mid[0], after[1] - mid[1])

        # UP = (-1, 0)
        # DOWN = (1, 0)
        # LEFT = (0, -1)
        # RIGHT = (0, 1)

        match before_turn:
            case (0, -1): # Case left
                match after_turn:
                    case (0, -1): # Case left
                        turn = 'none'
                    case (-1, 0): # Case up
                        turn = 'right'
                    case (1, 0): # case down
                        turn = 'left'
            case (0, 1): # Case right
                match after_turn:
                    case (-1, 0): # case up
                        turn = 'left'
                    case (0, 1): # case right
                        turn = 'none'
                    case (1, 0): # case down
                        turn = 'right'
            case (-1, 0): # Case up
                match after_turn:
                    case (0, -1): # case left
                        turn = 'left'
                    case (-1, 0): # case up
                        turn = 'none'
                    case (0, 1): # case right
                        turn = 'right'
            case (1, 0): # Case down
                match after_turn:
                    case (0, 1): # case right
                        turn = 'left'
                    case (1, 0): # case down
                        turn = 'none'
                    case (0, -1): # case up
                        turn = 'right'

        angle += ANGLES[turn]

    anticlockwise = True
    loopcheck = AC_LOOPCHECK

    if angle < 0:
        anticlockwise = False
        loopcheck = C_LOOPCHECK

    print(f'Total angle turned: {angle}, anticlockwise: {anticlockwise}')

    total_inside = 0
    final_seen = set(seen)

    for i in range(1, len(seen) - 1):
        before = seen[i-1]
        mid = seen[i]

        before_turn = (mid[0] - before[0], mid[1] - before[1])

        directions = loopcheck[before_turn]

        for drow, dcol in directions:
            print(f'At {mid} considering {mid[0] + drow, mid[1] + dcol}')
            total_inside += BFS((mid[0] + drow, mid[1] + dcol), (n_rows, n_cols), final_seen)

    print("Finished")

    return total_inside


def BFS(coords, dims, final_seen):

    n_rows, n_cols = dims

    n_inside = 0
    BFS_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if coords in final_seen or not is_in_boundary(coords, n_rows, n_cols):
        return 0

    queue = deque([coords])
    final_seen.add(coords)

    while queue:
        row, col = queue.pop()
        print(f'{row, col} is inside!!')
        n_inside += 1

        for drow, dcol in BFS_DIRECTIONS:
            nrow, ncol = row + drow, col + dcol
            if (nrow, ncol) not in final_seen and is_in_boundary((nrow, ncol), n_rows, n_cols):
                queue.appendleft((nrow, ncol))
                final_seen.add((nrow, ncol))

    return n_inside

def is_in_boundary(coords, n_rows, n_cols):
    if coords[0] >= 0 and coords[0] < n_rows and coords[1] >= 0 and coords[1] < n_cols:
        return True

    return False

if __name__ == '__main__':

    file = './data.txt'

    print(mainb(file))