from utils.utils import read_file
from collections import Counter
import re

def get_result(string):

    first, second = string.split(',')

    first_val = int(first[4:])
    second_val = int(second[:-1])

    return first_val * second_val

def parse(line):

    pattern = r"mul\([0-9]+,[0-9]+\)"

    all_results = re.findall(pattern, line)

    total = 0
    for result in all_results:
        total += get_result(result)

    return total

def parse_do_dont(line, active):
    pattern = r"mul\([0-9]+,[0-9]+\)|do\(\)|don't\(\)"

    all_results = re.findall(pattern, line)

    total = 0
    for result in all_results:
        if result == "do()":
            active = 1
        elif result == "don't()":
            active = 0
        else:
            total += get_result(result) * active

    return total, active


def main1_impl(tuple_):

    full_data = tuple_

    total = 0

    for line in full_data:
        total += parse(line)

    return total

def main2_impl(tuple_):

    full_data = tuple_

    total = 0
    active = 1

    for line in full_data:
        add_to_total, active = parse_do_dont(line, active)
        total += add_to_total

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
