from typing import NamedTuple
import math
import itertools

class LRTuple(NamedTuple):
    left: str
    right: str

def maina(file):
    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    total_steps = 0
    LRdestination = {}

    with open(file, 'r') as f:

        steps = f.readline().strip()

        f.readline()

        for line in f:

            LRdestination[line[:3]] = LRTuple(line[7:10], line[12:15])

    current = 'AAA'
    step_index = 0

    while current != "ZZZ":
        print(current, step_index, steps[step_index])
        if steps[step_index] == 'L':
            current = LRdestination[current].left
        else:
            current = LRdestination[current].right

        step_index = (step_index + 1) % len(steps)
        total_steps += 1

    return total_steps

def mainb(file):

    # Read in all lines of the file as tuples
    # Sort based on the hand strength
    # then multiply rank by bid
    total_steps = 0
    LRdestination = {}

    with open(file, 'r') as f:

        steps = f.readline().strip()

        f.readline()

        for line in f:
            LRdestination[line[:3]] = LRTuple(line[7:10], line[12:15])

    current_list = []

    for current in LRdestination.keys():
        if current[-1] == 'A':
            current_list.append(current)

    print(current_list)

    reached = []
    product = 1

    # for current in current_list:
    #     step_index = 0
    #     total_steps = 0
    #     reached = 0
    #     print(current)
    #     while total_steps < 100000:
    #         if steps[step_index] == 'L':
    #             current = LRdestination[current].left
    #         else:
    #             current = LRdestination[current].right
    #
    #         step_index = (step_index + 1) % len(steps)
    #         total_steps += 1
    #
    #         if current[-1] == 'Z':
    #             print(total_steps - reached)
    #             reached = total_steps
    #
    #


    # for val in reached:
    #     product *= val

    for current in current_list:
        step_index = 0
        total_steps = 0

        while current[-1] != 'Z':
            if steps[step_index] == 'L':
                current = LRdestination[current].left
            else:
                current = LRdestination[current].right

            step_index = (step_index + 1) % len(steps)
            total_steps += 1

            if current[-1] == 'Z':
                reached.append(total_steps)

    product = 1

    res = [(a, b) for idx, a in enumerate(reached) for b in reached[idx + 1:]]

    for pair in res:
        print(pair)
        print(math.gcd(pair[0], pair[1]))


    for val in reached:
        product *= val

    return product / 269**5

def check_list_ZZZ(list):
    for current in list:
        if current[-1] != 'Z':
            return False

    return True

if __name__ == '__main__':

    file = './data.txt'

    print(mainb(file))