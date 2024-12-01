from typing import NamedTuple
import math
import itertools
import re


PATTERN = r"\s*(-*\d+)"

def calculate_next_value(line):

    last_number = []

    while True:
        print(line)
        last_number.append(line[-1])
        line = line_difference(line)
        if is_all_zeros(line):
            break

    return sum(last_number)

def calculate_previous_value(line):

    first_number = []

    while True:
        print(line)
        first_number.append(line[0])
        line = line_difference(line)
        if is_all_zeros(line):
            break

    sum = 0
    for i, val in enumerate(first_number):

        if (i % 2) == 0:
            sum += val
        else:
            sum -= val

    return sum

def line_difference(line):

    difference = []

    for i in range(1, len(line)):
        difference.append(line[i] - line[i-1])

    return difference

def is_all_zeros(line):

    for num in line:
        if num != 0:
            return False

    return True


def maina(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    sum = 0

    with open(file, 'r') as f:

        for line in f:

            line_int = [int(i) for i in re.findall(PATTERN, line.strip())]
            next_value = calculate_next_value(line_int)
            print(next_value)
            sum += next_value

    return sum

def mainb(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    sum = 0

    with open(file, 'r') as f:

        for line in f:

            line_int = [int(i) for i in re.findall(PATTERN, line.strip())]
            next_value = calculate_previous_value(line_int)
            print(next_value)
            sum += next_value

    return sum

if __name__ == '__main__':

    file = './data.txt'

    print(mainb(file))