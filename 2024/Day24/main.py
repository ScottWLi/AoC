from utils.utils import read_file, Grid, Coordinate
from utils.utils import DIRECTIONS, GridPointer
from collections import Counter, deque
from functools import cmp_to_key, cache
from itertools import product, combinations
import re
import math
from typing import NamedTuple
from collections import defaultdict
import heapq
from itertools import chain, combinations
from typing import NamedTuple

def XOR(val1, val2):
    if val1 == val2:
        return '0'
    else:
        return '1'

def AND(val1, val2):
    if val1 == '1' and val2 == '1':
        return '1'
    else:
        return '0'

def OR(val1, val2):
    if val1 == '1' or val2 == '1':
        return '1'
    else:
        return '0'

OPERATOR_TO_FUNCTION = {
    'XOR': XOR,
    'AND': AND,
    'OR': OR
}

def binary_list_to_int(list_, instantiated):
    _ret = [instantiated[output] for output in list_[::-1]]
    ret = int(''.join(_ret), 2)

    return ret

def get_output_values(outputs, starting_values, dependencies):
    instantiated = starting_values.copy()

    seen_dependencies = set()

    for output in outputs:
        queue = deque([output])
        while queue:
            front = queue.popleft()

            if front in seen_dependencies:
                raise RecursionError("Error")

            if front in instantiated:
                continue

            dependency_1, operator, dependency_2 = dependencies[front]

            if dependency_1 not in instantiated or dependency_2 not in instantiated:
                queue.appendleft(front)
                if dependency_1 not in instantiated:
                    queue.appendleft(dependency_1)
                if dependency_2 not in instantiated:
                    queue.appendleft(dependency_2)
            else:
                instantiated[front] = OPERATOR_TO_FUNCTION[operator](instantiated[dependency_1], instantiated[dependency_2])

    return binary_list_to_int(outputs, instantiated)


def main1_impl(tuple_):
    # Parse all the inputs:
    # State is represented with a dictionary
    # If instantiated, then it exists in the dictionary

    # We have a dependency tree:
    # Represent this as a map of wire: dependencies
    #
    # Loop through the list of all gates
    # If instantiated already, do nothing
    # Otherwise, queue is wire output from gate:
    #   While queue:
    #     Pop front
    #       If its dependencies are instantiated, resolve it
    #     Otherwise
    #       Add back to front of queue
    #       Add dependencies to front of queue
    #
    # Resolve finish condition

    input_split_index = next(idx for idx, value in enumerate(tuple_) if value == '')

    INITIAL_VALUES = {}

    for line in tuple_[:input_split_index]:
        key, value = line.split(': ')
        INITIAL_VALUES[key] = value

    STARTING_DEPENDENCIES = dict() # Map dependent to a list of its gate dependencies
    for line in tuple_[input_split_index+1:]:
        val1, operator, val2, _, dependent = line.split(' ')
        STARTING_DEPENDENCIES[dependent] = (val1, operator, val2)

    z_outputs = tuple(sorted((key for key in STARTING_DEPENDENCIES.keys() if key[0] == 'z')))
    x_outputs = tuple(sorted((key for key in STARTING_DEPENDENCIES.keys() if key[0] == 'x')))
    y_outputs = tuple(sorted((key for key in STARTING_DEPENDENCIES.keys() if key[0] == 'y')))

    ret = get_output_values(z_outputs, INITIAL_VALUES, STARTING_DEPENDENCIES)

    return ret

def main2_impl(tuple_):
    return

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
