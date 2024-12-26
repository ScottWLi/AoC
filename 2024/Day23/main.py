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

def main1_impl(tuple_):
    # dictionary that maps node: set (connections)

    # Loop over keys that contain a t
    # Choose 2 from connections, and check if those 2 conenct
    # Save connections in a set of sorted keys
    # solution.add(sorted(key1, key2, key3))

    connections = defaultdict(set)

    for connection in tuple_:
        comp_a, comp_b = connection.split('-')
        connections[comp_a].add(comp_b)
        connections[comp_b].add(comp_a)

    solutions = set()
    for comp_a, value in connections.items():
        if comp_a[0] != 't':
            continue
        for comp_b, comp_c in combinations(value, 2):
            if comp_c in connections[comp_b]:
                solutions.add(tuple(sorted((comp_a, comp_b, comp_c))))

    return len(solutions)

def next_tuples(connection_dict, interconnected_graph):

    new_members = set.intersection(*(connection_dict[item] for item in interconnected_graph))

    ret = set()
    for member in new_members:
        ret.add(tuple(sorted(interconnected_graph + (member, ))))

    return ret

def main2_impl(tuple_):
    connections = defaultdict(set)

    connected_graphs = defaultdict(set)

    for connection in tuple_:
        comp_a, comp_b = connection.split('-')
        connections[comp_a].add(comp_b)
        connections[comp_b].add(comp_a)

        connected_graphs[2].add(tuple(sorted((comp_a, comp_b))))

    graph_size = 3
    while len(connected_graphs[graph_size-1]) > 0:
        for item in connected_graphs[graph_size - 1]:
            connected_graphs[graph_size].update(next_tuples(connections, item))

        graph_size += 1

    answer = ','.join(list(connected_graphs[graph_size-2])[0])

    return answer

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
