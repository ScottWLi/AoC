import posix
from ast import literal_eval
from ssl import TLSVersion

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
from itertools import chain
from typing import NamedTuple

class Program:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

        self.pointer = 0
        self.output = []

    @staticmethod
    def literal_operand(value):
        return int(value)

    def combo_operand(self, value):
        if value in {'0', '1', '2', '3'}:
            return Program.literal_operand(value)
        elif value == '4':
            return self.a
        elif value == '5':
            return self.b
        elif value == '6':
            return self.c
        elif value == '7' :
            raise ValueError("Operand 7 is reserved and should not appear in valid programs")
        else:
            raise ValueError(f"Unrecognised value {value}")

    def xdv(self, operand):
        self.pointer += 2
        return math.floor(self.a / (2 ** self.combo_operand(operand)))

    def adv(self, operand):
        self.a = self.xdv(operand)

    def bxl(self, operand):
        self.pointer += 2
        self.b = self.b ^ Program.literal_operand(operand)

    def bst(self, operand):
        self.pointer += 2
        self.b = (self.combo_operand(operand) % 8)

    def jnz(self, operand):
        if self.a != 0 and self.pointer != Program.literal_operand(operand):
            self.pointer = Program.literal_operand(operand)
        else:
            self.pointer += 2

    def bxc(self, operand):
        self.b = self.b ^ self.c
        self.pointer += 2

    def out(self, operand):
        self.output.append(str(self.combo_operand(operand) % 8))
        self.pointer += 2

    def bdv(self, operand):
        self.b = self.xdv(operand)

    def cdv(self, operand):
        self.c = self.xdv(operand)

    opcode = {
        '0': adv,
        '1': bxl,
        '2': bst,
        '3': jnz,
        '4': bxc,
        '5': out,
        '6': bdv,
        '7': cdv
    }

    def run_program(self, program):

        program_len = len(program)

        while self.pointer < program_len:
            opcode = program[self.pointer]
            operand = program[self.pointer + 1]

            Program.opcode[opcode](self, operand)

        return self.output

    def __str__(self) :
        return (f"Program State:\n"
                f"  a: {self.a}\n"
                f"  b: {self.b}\n"
                f"  c: {self.c}\n"
                f"  pointer: {self.pointer}\n"
                f"  output: {self.output}")

def main1_impl(tuple_):

    a = int(tuple_[0][12:])
    b = int(tuple_[1][12:])
    c = int(tuple_[2][12:])
    program_list = tuple_[4][9:].split(',')

    program = Program(a, b, c)

    output = program.run_program(program_list)

    return ','.join(output)

def main2_impl(tuple_):
    k = 0 * 8 + 3 * 8 ** 2

    b = int(tuple_[1][12 :])
    c = int(tuple_[2][12 :])
    program_list = tuple_[4][9 :].split(',')

    queue = [[]]

    program_list_int = [
        6,  #
        5,  #
        6,  #
        2,  #
        4,  #
        5,  #
        7,  #
        4,
        0,
        4,
        2,
        5,
        7,
        2,
        7,
        7
    ]
    answers = []
    seen = set()

    while queue:
        front = queue.pop()

        if len(front) == 16:
            continue

        for i in range(8):
            new_front = front + [i]
            max_power = len(new_front)

            total = 0
            for idx, val in enumerate(new_front):
                total += val * 8**(max_power - 1 - idx)

            if total in seen:
                continue

            seen.add(total)

            program = Program(total, b, c)

            output = program.run_program(program_list)

            output_matches = True
            for check_idx in range(max_power):
                if output[-(check_idx+1)] != program_list[-(check_idx+1)]:
                    output_matches = False
                    break

            if output_matches:
                print(f'{output} matches {program_list} for last {max_power}')
                print(new_front)
                queue.append(new_front)
                if max_power == 16:
                    answers.append(total)

    return min(answers)

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
