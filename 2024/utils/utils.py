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

    def __rmul__(self, value):
        return self * value

    def __sub__(self, other):
        return Coordinate(self.row - other.row, self.column - other.column)

    def __truediv__(self, value):
        return Coordinate(self.row / value, self.column / value)

    def __floordiv__(self, value):
        return Coordinate(self.row // value, self.column // value)

    def __bool__(self):
        return self.row != 0 or self.column != 0

    def manhattan(self, other):
        diff = self - other
        return abs(diff.row) + abs(diff.column)


class DIRECTIONS(Enum):
    UP = Coordinate(-1, 0)
    DOWN = Coordinate(1, 0)
    RIGHT = Coordinate(0, 1)
    LEFT = Coordinate(0, -1)
    UP_RIGHT = UP + RIGHT
    UP_LEFT = UP + LEFT
    DOWN_LEFT = DOWN + LEFT
    DOWN_RIGHT = DOWN + RIGHT

    @classmethod
    def simple_directions(cls):
        return [cls.UP, cls.DOWN, cls.RIGHT, cls.LEFT]


class Grid:
    def __init__(self, grid, as_int = False):
        if as_int:
            self.grid = [list(map(int,row)) for row in grid]
        else:
            self.grid = [list(row) for row in grid]

    def __contains__(self, coordinate):
        return ((coordinate.row >= 0 and coordinate.row < len(self.grid))
                and (coordinate.column >= 0 and coordinate.column < len(self.grid[0])))

    def __getitem__(self, coordinate):
        return self.grid[coordinate.row][coordinate.column]

    def __setitem__(self, coordinate, value):
        self.grid[coordinate.row][coordinate.column] = value

    def dims(self):
        return len(self.grid), len(self.grid[0])

    def find(self, value):
        for row_idx, row in enumerate(self.grid):
            for col_idx, char in enumerate(row):
                if char == value:
                    return Coordinate(row_idx, col_idx)

    def find_all(self, value):
        ret = []
        for row_idx, row in enumerate(self.grid):
            for col_idx, char in enumerate(row):
                if char == value:
                    ret.append(Coordinate(row_idx, col_idx))

        return ret

    def count(self, value):
        count = 0
        for row in self.grid:
            for char in row:
                if char == value:
                    count += 1

        return count

    def __str__(self) :
        return "\n".join("".join(map(str, row)) for row in self.grid)


class GridPointer:
    def __init__(self, coordinate, direction):
        self.location: Coordinate = coordinate
        self.direction: DIRECTIONS = direction

    def __eq__(self, other) :
        if not isinstance(other, GridPointer) :
            return NotImplemented
        return self.location == other.location and self.direction == other.direction

    def __hash__(self) :
        return hash((self.location, self.direction))

    def in_front_of(self):
        return self.location + self.direction.value

    def turn_right(self):
        turn = {
            DIRECTIONS.UP: DIRECTIONS.RIGHT,
            DIRECTIONS.RIGHT: DIRECTIONS.DOWN,
            DIRECTIONS.DOWN: DIRECTIONS.LEFT,
            DIRECTIONS.LEFT: DIRECTIONS.UP
        }

        return GridPointer(self.location, turn[self.direction])

    def __repr__(self) :
        return f"GridPointer(location={self.location}, direction={self.direction})"

    def __str__(self) :
        return f"GridPointer at {self.location} facing {self.direction.name}"

    def walk(self):
        return GridPointer(self.location + self.direction.value, self.direction)
