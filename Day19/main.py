from typing import NamedTuple
import math
import itertools
import re
from functools import cache
from collections import deque
import heapq
import numpy as np

PATTERN = r"{(-*\d+)}"
WORKFLOW_PATTERN = r"[a-zA-Z]*{(.*)}"
NAME_PATTERN = r"([a-zA-Z]+){"
PART_PATTERN = r"[a-zA-Z]=(\d+)"


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int

    def satisfies_criteria(self, criteria):
        match criteria.operator:
            case '>':
                if self.__getattribute__(criteria.part) > criteria.value:
                    return True
                else:
                    return False
            case '<':
                if self.__getattribute__(criteria.part) < criteria.value:
                    return True
                else:
                    return False
            case _:
                return -1

    def part_value(self):
        return self.x + self.m + self.a + self.s


class Criteria(NamedTuple):

    part: str
    operator: str
    value: int
    next_workflow: str


class Range(NamedTuple):
    min: int
    max: int

    def intersect_criteria(self, operator, value):
        match operator:
            case '>':
                if self.min > value and self.max > value:
                    return self
                elif self.min < value < self.max:
                    return Range(value + 1, self.max)
                else:
                    return None
            case '<':
                if self.min > value and self.max > value:
                    return None
                elif self.min < value < self.max:
                    return Range(self.min, value-1)
                else:
                    return self
            case _:
                return -1

    def disjoint_criteria(self, operator, value):
        match operator:
            case '>':
                if self.min > value and self.max > value:
                    return None
                elif self.min < value < self.max:
                    return Range(self.min, value)
                else:
                    return self
            case '<':
                if self.min > value and self.max > value:
                    return self
                elif self.min < value < self.max:
                    return Range(value, self.max)
                else:
                    return None
            case _:
                return -1

    def size(self):
        return self.max - self.min + 1


class Part_Range(NamedTuple):

    x: Range
    m: Range
    a: Range
    s: Range

    def is_empty(self):
        if not self.x or not self.m or not self.a or not self.s:
            return True
        return False

    def intersect_criteria(self, criteria):
        range = self.__getattribute__(criteria.part)
        new_range = range.intersect_criteria(criteria.operator, criteria.value)
        self_as_dict = self._asdict()
        self_as_dict[criteria.part] = new_range

        return Part_Range(**self_as_dict)

    def disjoint_criteria(self, criteria):
        range = self.__getattribute__(criteria.part)
        new_range = range.disjoint_criteria(criteria.operator, criteria.value)
        self_as_dict = self._asdict()
        self_as_dict[criteria.part] = new_range

        return Part_Range(**self_as_dict)

    def combinations(self):
        return self.x.size() * self.m.size() * self.a.size() * self.s.size()


class QueueMember(NamedTuple):
    destination: str
    part_range: Part_Range

def process_workflow(line, workflow):
    criteria_list = []
    name_match = re.match(NAME_PATTERN, line)
    workflow_match = re.match(WORKFLOW_PATTERN, line)

    name = name_match.group(1)
    criterias = workflow_match.group(1).split(',')

    for criteria in criterias:
        criteria_split = criteria.split(':')
        if len(criteria_split) == 1:
            criteria_list.append(criteria_split[0])
        else:
            part = criteria_split[0][0]
            operator = criteria_split[0][1]
            value = int(criteria_split[0][2:])
            new_workflow =  criteria_split[1]
            criteria_obj = Criteria(part, operator, value, new_workflow)
            criteria_list.append(criteria_obj)

    workflow[name] = criteria_list

    return


def process_part(line):
    line = line[1:-1]
    parts = line.split(',')
    parts_values = []

    for part in parts:
        match = re.match(PART_PATTERN, part)
        parts_values.append(int(match.group(1)))

    return Part(parts_values[0], parts_values[1], parts_values[2], parts_values[3])


def maina(file):

    workflows = {}
    parts = []

    with open(file, 'r') as f:
        for line in f:
            if line == '\n':
                break

            process_workflow(line.strip(), workflows)

        for line in f:
            parts.append(process_part(line.strip()))

    total_accepted = 0

    for part in parts:
        # print(f'Considering part: {part}')
        current = 'in'
        looping = True
        tracker = 0
        while looping and tracker < 10:
            if current in set(['A', 'R']):
                # print(current)
                looping = False
                if current == 'A':
                    total_accepted += part.part_value()
                break
            workflow = workflows[current]
            # print('----------')
            # print(f'Name of workflow: {current}')
            # print(f'Workflow: {workflow}')
            for criteria in workflow:
                # print(f'Considering {criteria}')
                if isinstance(criteria, str):
                    # print(f'{criteria} is just a string. It is the next current')
                    current = criteria
                    break
                if part.satisfies_criteria(criteria):
                    # print(f'{criteria} satisfied by {part}')
                    current = criteria.next_workflow
                    break
            tracker += 1


    return total_accepted


def mainb(file):

    workflows = {}

    with open(file, 'r') as f:
        for line in f:
            if line == '\n':
                break

            process_workflow(line.strip(), workflows)

    starting = Part_Range(Range(1, 4000), Range(1, 4000), Range(1, 4000), Range(1,4000))

    queue = deque([QueueMember('in', starting)])
    accepted_ranges = []
    total_accepted = 0

    # print('Starting')

    while queue:
        front = queue.popleft()
        dest = front.destination
        part_range = front.part_range
        # print('------------')
        # print(front)

        if dest in set(['A', 'R']):
            if dest == 'A':
                accepted_ranges.append(part_range)
            continue

        workflow = workflows[dest]
        # print(workflow)
        # print('----')
        for criteria in workflow:
            # print('--')
            # print(criteria)
            if isinstance(criteria, str):
                if not part_range.is_empty():
                    # print(f'Continuation portion: {part_range}')
                    queue.append(QueueMember(criteria, part_range))
                break
            else:
                intersect_range = part_range.intersect_criteria(criteria)
                # print(f'Rejected portion: {intersect_range}')
                if not intersect_range.is_empty():
                    queue.append(QueueMember(criteria.next_workflow, intersect_range))

                part_range = part_range.disjoint_criteria(criteria)
                # print(f'Continuation portion: {part_range}')

    print(accepted_ranges)

    for part_range in accepted_ranges:
        total_accepted += part_range.combinations()

    return total_accepted


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))
    #
    # part_range = Part_Range(Range(1, 4000), Range(1, 4000), Range(1, 4000), Range(1, 4000))
    # test_criteria = Criteria(part='s', operator='<', value=1351, next_workflow='px')
    # print(part_range.intersect_criteria(test_criteria))