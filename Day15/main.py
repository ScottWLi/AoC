from typing import NamedTuple
import math
import itertools
import re
from functools import cache

PATTERN = r"\s*(-*\d+)"

def hash_algorithm(string):
    total = 0
    for char in string:
        total = parse_character(char, total)

    return total

def parse_character(char, total):
    total += ord(char)
    total *= 17
    total = total % 256

    return total

def maina(file):
    total = 0

    with open(file, 'r') as f:
        string = f.readline()

    substrings = string.split(',')

    for substring in substrings:
        value = hash_algorithm(substring)
        total += value
        # print(f'{substring} = {value}')

    return total

def mainb(file):

    boxes = {}

    total = 0

    with open(file, 'r') as f:
        string = f.readline()

    substrings = string.split(',')

    for substring in substrings:
        if '-' in substring:
            code = substring.split('-')[0]
            hash_code = hash_algorithm(code)
            if hash_code in boxes:
                for lens in boxes[hash_code]:
                    if lens[0] == code:
                        boxes[hash_code].remove(lens)
        elif '=' in substring:
            code, lens = tuple(substring.split('='))
            hash_code = hash_algorithm(code)
            if hash_code not in boxes:
                boxes[hash_code] = [(code, int(lens))]
            else:
                new_lens = True
                for i, lens_tuple in enumerate(boxes[hash_code]):
                    if lens_tuple[0] == code:
                        boxes[hash_code][i] = (code, int(lens))
                        new_lens = False
                        break
                if new_lens:
                    boxes[hash_code].append((code, int(lens)))
        # print(boxes)

    for box_no, lens_list in boxes.items():
        for position, lens_tuple in enumerate(lens_list):
            total += (box_no+1) * (position+1) * lens_tuple[1]


    return total

if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))