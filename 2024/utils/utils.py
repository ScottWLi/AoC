from typing import NamedTuple
from enum import Enum

def read_file(file_path):
    with open(file_path, 'r') as f:
        data = tuple(line.strip() for line in f)

    return data


class Coordinate(NamedTuple):
    row: int
    column: int

    def __add__(self, other):
        return Coordinate(self.row + other.row, self.column + other.column)

    def __mul__(self, value):
        return Coordinate(self.row * value, self.column * value)


class DIRECTIONS(Enum):
    UP = Coordinate(-1, 0)
    DOWN = Coordinate(1, 0)
    RIGHT = Coordinate(0, 1)
    LEFT = Coordinate(0, -1)
    UP_RIGHT = UP + RIGHT
    UP_LEFT = UP + LEFT
    DOWN_LEFT = DOWN + LEFT
    DOWN_RIGHT = DOWN + RIGHT


class Grid:
    def __init__(self, grid):
        self.grid = grid

    def __contains__(self, coordinate):
        return ((coordinate.row >= 0 and coordinate.row < len(self.grid))
                and (coordinate.column >= 0 and coordinate.column < len(self.grid[0])))

    def __getitem__(self, coordinate):
        return self.grid[coordinate.row][coordinate.column]

    def dims(self):
        return (len(self.grid), len(self.grid[0]))