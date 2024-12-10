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


class FileBlock(NamedTuple):
    index: int
    len: int


def main1_impl(tuple_):
    disk_map = tuple_[0]

    file_id = 0
    is_id = True

    expanded = []

    for num in disk_map:
        if is_id:
            expanded.extend([str(file_id)] * int(num))
            file_id += 1
        else:
            expanded.extend(['.'] * int(num))
        is_id = not is_id

    front_ptr = 0
    back_ptr = len(expanded) - 1

    while back_ptr > front_ptr:
        if expanded[front_ptr] != '.':
            front_ptr += 1
        elif expanded[back_ptr] == '.':
            back_ptr -= 1
        else:
            expanded[front_ptr] = expanded[back_ptr]
            expanded[back_ptr] = '.'
            front_ptr += 1
            back_ptr -= 1

    total = 0

    for idx, val in enumerate(expanded):
        if val == '.':
            break
        total += idx * int(val)

    return total

def main2_impl(tuple_):
    disk_map = tuple_[0]

    file_id = 0
    is_id = True

    expanded = []
    empty_blocks = []
    file_blocks = dict()
    #: This maps empty blocks by having length _key_ to a heapq of indices
    end_idx = 0

    for num in disk_map:
        if is_id:
            expanded.extend([str(file_id)] * int(num))
            file_blocks[file_id] = FileBlock(end_idx, int(num))
            file_id += 1
        else:
            expanded.extend(['.'] * int(num))
            empty_blocks.append(FileBlock(end_idx, int(num)))
        end_idx += int(num)
        is_id = not is_id

    for file_id_ in reversed(range(file_id)):
        file_block = file_blocks[file_id_]

        index = file_block.index
        len = file_block.len

        first_empty_block_idx = next(
            (idx for idx, empty_block in enumerate(empty_blocks)
             if empty_block.len >= file_block.len and index > empty_block.index),
            None)

        if first_empty_block_idx != 0 and not first_empty_block_idx:
            continue

        empty_block = empty_blocks[first_empty_block_idx]

        for i in range(len):
            expanded[empty_block.index + i] = file_id_
            expanded[index + i] = '.'

        if empty_block.len == len:
            empty_blocks.pop(first_empty_block_idx)
        else:
            empty_blocks[first_empty_block_idx] = FileBlock(empty_block.index + len, empty_block.len - file_block.len)

    total = 0

    for idx, val in enumerate(expanded):
        if val == '.':
            continue
        total += idx * int(val)

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
