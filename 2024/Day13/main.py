import posix

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

class Button(NamedTuple):
    x: int
    y: int

class Game(NamedTuple):
    a: Button
    b: Button
    prize: Button


def parse_input(input, p2 = 0):

    ret = []
    a = b = prize = None

    BUTTON_A = re.compile("Button A:")
    BUTTON_B = re.compile("Button B:")
    PRIZE = re.compile("Prize:")
    X = re.compile(r"X[+=]([0-9]+)")
    Y = re.compile(r"Y[+=]([0-9]+)")

    for row in input:
        if row == "":
            a = b = prize = None
            continue

        x = X.search(row)
        y = Y.search(row)

        if BUTTON_A.match(row):
            a = Button(int(x.group(1)), int(y.group(1)))
        elif BUTTON_B.match(row):
            b = Button(int(x.group(1)), int(y.group(1)))
        elif PRIZE.match(row):
            prize = Button(int(x.group(1)) + p2, int(y.group(1)) + p2)
            ret.append(Game(a, b, prize))
        else:
            raise ValueError(f"Unable to match {row}")

    return ret


def main1_impl(tuple_):

    games = parse_input(tuple_)

    total = 0
    for game in games:
        a = game.a
        b = game.b
        p = game.prize

        i = (p.x * b.y - p.y * b.x) / (a.x * b.y - a.y * b.x)
        j = (p.x - i * a.x) / b.x

        if i.is_integer() and j.is_integer():
            total += int(i) * 3 + int(j)

            if (int(i) * a.x + int(j) * b.x != p.x) or (int(i) * a.y + int(j) * b.y != p.y):
                raise ValueError(f"Unexpected error for {game}")

    return total

def main2_impl(tuple_):

    games = parse_input(tuple_, 10000000000000)

    total = 0
    for game in games:
        a = game.a
        b = game.b
        p = game.prize

        i = (p.x * b.y - p.y * b.x) / (a.x * b.y - a.y * b.x)
        j = (p.x - i * a.x) / b.x

        if i.is_integer() and j.is_integer():
            total += int(i) * 3 + int(j)

            if (int(i) * a.x + int(j) * b.x != p.x) or (int(i) * a.y + int(j) * b.y != p.y):
                raise ValueError(f"Unexpected error for {game}")

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
