from typing import NamedTuple
import math
import itertools
import re
from functools import cache
from collections import deque


class XYZCoord(NamedTuple):
    x: int
    y: int
    z: int

    def is_on_top_of(self, floor):
        if (floor[self.x][self.y] == (self.z - 1)):
            return True
        return False

    def is_on_top_of_brick(self, brick):
        if (brick.start.x <= self.x <= brick.end.x) and (brick.start.y <= self.y <= brick.end.y) and (brick.end.z == self.z - 1):
            return True

        return False

    def __str__(self):
        return f'x: {self.x}, y: {self.y}, z: {self.z}'


class Brick:

    def __init__(self, start:XYZCoord, end: XYZCoord, id: int):
        self.start = start
        self.end = end
        self.id = id

    def fall(self):
        start_dict = self.start._asdict()
        end_dict = self.end._asdict()
        start_dict['z'] -= 1
        end_dict['z'] -= 1

        self.start = XYZCoord(**start_dict)
        self.end = XYZCoord(**end_dict)

    def can_fall(self, floor):
        block_list = self.get_blocks()
        for block in block_list:
            if block.is_on_top_of(floor):
                return False

        return True

    def get_blocks(self):
        #if vertical, returns only the bottom block

        blocks = set()
        template = {'x': self.start.x,
                    'y': self.start.y,
                    'z': self.start.z}

        if self.start.z != self.end.z:
            template['z'] = min(self.end.z, self.start.z)
            blocks.add(XYZCoord(**template))
        else:
            blocks.add(XYZCoord(**template))

            dimensions = ['x', 'y']

            for dim in dimensions:
                for i in range(getattr(self.end,dim), getattr(self.start,dim), -1):
                    template[dim] = i
                    blocks.add(XYZCoord(**template))

        return blocks

    def update_floor(self, floor):

        template = {'x': self.start.x,
                    'y': self.start.y,
                    'z': self.start.z}
        floor[template['x']][template['y']] = self.end.z
        dimensions = ['x', 'y']

        for dim in dimensions:
            for i in range(getattr(self.end,dim), getattr(self.start,dim), -1):
                template[dim] = i
                floor[template['x']][template['y']] = self.end.z

    def is_on_top_of(self, brick2):
        block_list = self.get_blocks()
        for block in block_list:
            if block.is_on_top_of_brick(brick2):
                return True

        return False


    def __str__(self):
        return f'{self.id} with start {self.start} and end {self.end}'

def input_reader(string):
    string_list = string.split(',')
    string_list_as_int = tuple([int(x) for x in string_list])

    return XYZCoord(*string_list_as_int)


def can_disintegrate_block(brick_id, supports, is_supported_by):

    can_disintegrate = True
    # print(f'Considering brick {brick.id}')
    if brick_id in supports:
        bricks_supported = supports[brick.id]
        for brick_supported_id in bricks_supported:
            if len(is_supported_by[brick_supported_id]) <= 1:
                can_disintegrate = False
                break

    return can_disintegrate


def maina(file):
    # Create a list of all bricks
    # Make all bricks fall
    #   If brick is sitting on top of another brick, do nothing
    #   Else reduce z coordinate by 1
    # Check how many bricks sit on more than 1 brick
    brick_lookup = {}
    max_x = 0
    max_y = 0
    id = 0

    with open(file, 'r') as f:
        for line in f:
            split_line = line.strip().split('~')
            start_coord = input_reader(split_line[0])
            end_coord = input_reader(split_line[1])

            max_x = max(max_x, end_coord.x)
            max_y = max(max_y, end_coord.y)

            brick_lookup[id] = Brick(start_coord, end_coord, id)

            id += 1

    brick_list = list(brick_lookup.values())
    brick_list.sort(key=lambda brick: brick.start.z)

    # rows of floor are x
    # eg floor[x][y]

    floor = [[0] * (max_y + 1)for _ in range(max_x + 1)]

    bricks_falling = brick_list.copy()

    for brick in bricks_falling:
        while brick.can_fall(floor):
            brick.fall()
        brick.update_floor(floor)

    supports = {}
    is_supported_by = {}

    for i in range(len(brick_list)):
        for j in range(i):
            brick1 = brick_list[i]
            brick2 = brick_list[j]

            if brick1.is_on_top_of(brick2):
                if brick2.id not in supports:
                    supports[brick2.id] = set([brick1.id])
                else:
                    supports[brick2.id].add(brick1.id)
                if brick1.id not in is_supported_by:
                    is_supported_by[brick1.id] = set([brick2.id])
                else:
                    is_supported_by[brick1.id].add(brick2.id)

            if brick2.is_on_top_of(brick1):
                if brick1.id not in supports:
                    supports[brick1.id] = set([brick2.id])
                else:
                    supports[brick1.id].add(brick2.id)
                if brick2.id not in is_supported_by:
                    is_supported_by[brick2.id] = set([brick1.id])
                else:
                    is_supported_by[brick2.id].add(brick1.id)


    n_disintegrated = 0

    for brick in brick_list:
        if can_disintegrate_block(brick.id, supports, is_supported_by):
            print(f'Brick {brick.id} can be disintegrated')
            n_disintegrated += 1

    for brick in brick_list:
        print(brick)

    # for key, value in is_supported_by.items():
    #     print('Brick')
    #     print(brick_lookup[key])
    #     print('Supported by')
    #     for val in value:
    #         print(brick_lookup[val])

    return n_disintegrated


def other_bricks_would_fall(brick_id, supports, is_supported_by):
    # Add the bricks brick_id supports to a queue
    # for each brick it supports, remove it from is_supported_by
    # if length of is_supported_by is zero, then add what it supports to the queue and repeat and uptick counter
    print(f'Calculating for {brick_id}')

    other_bricks = 0

    will_be_affected = {}

    queue = deque([brick_id])

    while queue:
        front = queue.popleft()
        if front in supports:
            front_supports = supports[front]
            for above in front_supports:
                if above in will_be_affected:
                    will_be_affected[above].append(front)
                else:
                    will_be_affected[above] = [front]
                if len(is_supported_by[above]) == len(will_be_affected[above]):
                    queue.append(above)
                    other_bricks += 1


    return other_bricks

def mainb(file):
    # Create a list of all bricks
    # Make all bricks fall
    #   If brick is sitting on top of another brick, do nothing
    #   Else reduce z coordinate by 1
    # Check how many bricks sit on more than 1 brick
    brick_lookup = {}
    max_x = 0
    max_y = 0
    id = 0

    with open(file, 'r') as f:
        for line in f:
            split_line = line.strip().split('~')
            start_coord = input_reader(split_line[0])
            end_coord = input_reader(split_line[1])

            max_x = max(max_x, end_coord.x)
            max_y = max(max_y, end_coord.y)

            brick_lookup[id] = Brick(start_coord, end_coord, id)

            id += 1

    brick_list = list(brick_lookup.values())
    brick_list.sort(key=lambda brick: brick.start.z)

    # rows of floor are x
    # eg floor[x][y]

    floor = [[0] * (max_y + 1)for _ in range(max_x + 1)]

    bricks_falling = brick_list.copy()

    for brick in bricks_falling:
        while brick.can_fall(floor):
            brick.fall()
        brick.update_floor(floor)

    supports = {}
    is_supported_by = {}

    for i in range(len(brick_list)):
        for j in range(i):
            brick1 = brick_list[i]
            brick2 = brick_list[j]

            if brick1.is_on_top_of(brick2):
                if brick2.id not in supports:
                    supports[brick2.id] = set([brick1.id])
                else:
                    supports[brick2.id].add(brick1.id)
                if brick1.id not in is_supported_by:
                    is_supported_by[brick1.id] = set([brick2.id])
                else:
                    is_supported_by[brick1.id].add(brick2.id)

            if brick2.is_on_top_of(brick1):
                if brick1.id not in supports:
                    supports[brick1.id] = set([brick2.id])
                else:
                    supports[brick1.id].add(brick2.id)
                if brick2.id not in is_supported_by:
                    is_supported_by[brick2.id] = set([brick1.id])
                else:
                    is_supported_by[brick2.id].add(brick1.id)


    n_total_fallen = 0

    for brick in brick_list:
        n_total_fallen += other_bricks_would_fall(brick.id, supports, is_supported_by)

    return n_total_fallen


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))
