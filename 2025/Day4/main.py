from utils.utils import read_file, Grid, Coordinate, DIRECTIONS
from collections import Counter
from utils.logging import logger

def main1_impl(tuple_):
    grid = Grid(tuple_)
    grid_copy = Grid(tuple_)

    logger.debug('\n' + str(grid))

    for direction in DIRECTIONS:
        logger.debug(direction.value)

    all_rolls = grid.find_all('@')

    total_rolls = 0
    for point in all_rolls:
        total_adjacents = 0
        for direction in DIRECTIONS:
            adjacent = point + direction.value
            if adjacent in grid and grid[adjacent] == '@':
                total_adjacents += 1
            if total_adjacents >= 4:
                break
        if total_adjacents < 4:
            total_rolls += 1
            grid_copy[point] = '.'

    logger.debug('\n' + str(grid_copy))

    return total_rolls, grid_copy.get_grid()

def main2_impl(tuple_):
    raw_grid = tuple_
    grid = Grid(raw_grid)

    starting_rolls = grid.count('@')

    total_rolls = 1
    while total_rolls > 0:
        total_rolls, raw_grid = main1_impl(raw_grid)

    final_rolls = Grid(raw_grid).count('@')

    return starting_rolls - final_rolls

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
