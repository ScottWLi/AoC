from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS, GridPointer
from collections import Counter
from functools import cmp_to_key
from itertools import product
import re

def main1_impl(tuple_):

    OPERATORS = ["+", "*"]

    answers, values = zip(*[
        (int(line.split(": ")[0]), tuple(map(int, line.split(": ")[1].split())))
        for line in tuple_
    ])

    possibles = Counter()
    for answer, value in zip(answers, values):
        n_operations = len(value) - 1
        for operators in product(OPERATORS, repeat=n_operations):
            local_total = value[0]
            for idx, operator in enumerate(operators):
                if operator == "+":
                    local_total += value[idx+1]
                elif operator == "*":
                    local_total *= value[idx+1]
                else:
                    raise Exception("Unexpected to get here")

            if local_total == answer:
                possibles[answer] += 1
                break

    total = 0

    for key, value in possibles.items():
        total += key * value

    return total


def main2_impl(tuple_):

    OPERATORS = ["+", "*", "|"]

    answers, values = zip(*[
        (int(line.split(": ")[0]), tuple(map(int, line.split(": ")[1].split())))
        for line in tuple_
    ])

    possibles = Counter()
    for answer, value in zip(answers, values):
        n_operations = len(value) - 1
        for operators in product(OPERATORS, repeat=n_operations):
            local_total = value[0]
            for idx, operator in enumerate(operators):
                if operator == "+":
                    local_total += value[idx+1]
                elif operator == "*":
                    local_total *= value[idx+1]
                elif operator == "|":
                    local_total = int(str(local_total) + str(value[idx+1]))
                else:
                    raise Exception("Unexpected to get here")

            if local_total == answer:
                possibles[answer] += 1
                break

    total = 0

    for key, value in possibles.items():
        total += key * value

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
