from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS
from collections import Counter
import re



def main1_impl(tuple_):

    grid = Grid(tuple_)

    n_rows, n_cols = grid.dims()

    directions = tuple(tuple(direction.value * (val) for val in range(4)) for direction in DIRECTIONS)

    total = 0

    for row_idx in range(n_rows):
        for col_idx in range(n_cols):
            base_coord = Coordinate(row_idx, col_idx)

            for direction_sequence in directions:
                base_string = ""
                coords_to_check = tuple(base_coord + direction for direction in direction_sequence)

                if all(element in grid for element in coords_to_check):
                    for element in coords_to_check:
                        base_string += grid[element]
                    if base_string == "XMAS":
                        total += 1

    return total

def main2_impl(tuple_):

    grid = Grid(tuple_)

    n_rows, n_cols = grid.dims()

    dir_back = (
        DIRECTIONS.UP_LEFT.value,
        Coordinate(0,0),
        DIRECTIONS.DOWN_RIGHT.value
    )

    dir_for = (
        DIRECTIONS.DOWN_LEFT.value,
        Coordinate(0,0),
        DIRECTIONS.UP_RIGHT.value
    )

    dirs = (dir_for, dir_back)

    ACCEPTED = set(("MAS", "SAM"))

    total = 0

    for row_idx in range(n_rows):
        for col_idx in range(n_cols):
            base_coord = Coordinate(row_idx, col_idx)

            crosses = []
            for direction_sequence in dirs:
                base_string = ""
                coords_to_check = tuple(base_coord + direction for direction in direction_sequence)

                if all(element in grid for element in coords_to_check):
                    for element in coords_to_check:
                        base_string += grid[element]
                    crosses.append(base_string)

            if len(crosses) == 2 and crosses[0] in ACCEPTED and crosses[1] in ACCEPTED:
                total += 1

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
