from typing import NamedTuple
import math
import itertools
import re
from functools import cache

PATTERN = r"\s*(-*\d+)"



def line_concat(springs, order):

    return springs + ' ' + order
@cache
def matches_first_order(springs, order):
    orders = order.split(',')
    first_order = int(orders[0])
    match = True

    if len(springs) < first_order:
        return False
    if len(orders) == 1:
        for i in range(first_order):
            if springs[i] not in set(['#', '?']):
                return False
    elif len(springs) <= first_order:
        return False
    else:
        for i in range(first_order):
            if springs[i] not in set(['#', '?']):
                return False
        if springs[first_order] not in set(['?', '.']):
            return False

    return True

@cache
def calculate_arrangements(line):

    springs, order = line.split(' ')
    orders = order.split(',')

    if not order:
        # print(f'nothing in {order}')
        if '#' in springs:
            return 0
        else:
            return 1
    elif not springs:
        return 0
    elif springs[0] == '.':
        # print(f'First char in {springs} is "."')
        return calculate_arrangements(line_concat(springs[1:], order))
    elif springs[0] == '#':
        # print(f'First char in {springs} is "#"')
        n_springs = int(orders[0])
        if matches_first_order(springs, order):
            # print(f'First order in {order} is in {springs}')
            if len(orders) == 1:
                return calculate_arrangements(line_concat(springs[n_springs:], ','.join(orders[1:])))
            else:
                return calculate_arrangements(line_concat(springs[n_springs+1:], ','.join(orders[1:])))
        else:
            # print(f'First order in {order} is not in {springs}')
            return 0
    elif springs[0] == '?':
        # print(f'First char in {springs} is "?"')
        return calculate_arrangements(line_concat(springs[1:], order)) + calculate_arrangements(line_concat('#' + springs[1:], order))
    else:
        # print(f'Should never get here')
        return -1

def maina(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    sum = 0

    with open(file, 'r') as f:
        for line in f:
            n_arrangements = calculate_arrangements(line.strip())
            print(f'{n_arrangements} arrangements in {line.strip()}')
            sum += n_arrangements

    return sum

def mainb(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    sum = 0
    # true_dict = {}
    # false_dict = {}

    with open(file, 'r') as f:
        for line in f:
            new_line = line.strip()
            springs, orders = new_line.split(' ')
            new_springs = '?'.join([springs for _ in range(5)])
            new_orders = ','.join([orders for _ in range(5)])
            new_new_line =line_concat(new_springs, new_orders)

            # n_arrangements = calculate_arrangements_cache(new_new_line, true_dict, false_dict)
            n_arrangements = calculate_arrangements(new_new_line)
            print(f'{n_arrangements} arrangements in {line.strip()}')

            sum += n_arrangements

    return sum


if __name__ == '__main__':

    file = './data.txt'
    # print(matches_first_order('#??#', '3'))
    # print(calculate_arrangements('?#??.?#.???#. 3,1,3'))

    print(maina(file))