from typing import NamedTuple
import math
import itertools
import re
from functools import cache
from collections import deque, Counter
import heapq
import numpy as np
from abc import ABC
import abc


class Module(ABC):

    def __init__(self, name, outputs):
        self.name = name
        self.outputs = outputs

    @abc.abstractmethod
    def broadcast(self):
        pass

    def __str__(self):
        return f'Name: {self.name}, Outputs: {self.outputs}'

    @abc.abstractmethod
    def is_original_state(self):
        pass


class Pulse(NamedTuple):
    type: str
    destination: str
    origin: str

    def process_pulse(self, modules, queue):
        if self.destination in modules:
            modules[self.destination].broadcast(self.type, queue, self.origin)

    def __str__(self):
        return f'{self.origin} -{self.type}-> {self.destination}'

class Broadcast(Module):

    def broadcast(self, input, queue, *args):
        for module in self.outputs:
            queue.append(Pulse(input, module, self.name))

    def is_original_state(self):
        return True

class Flfl(Module):

    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.off = True


    def broadcast(self, input, queue, *args):
        if input == 'low':
            self.off = not self.off
            for module in self.outputs:
                if self.off:
                    queue.append(Pulse('low', module, self.name))
                else:
                    queue.append(Pulse('high', module, self.name))

    def is_original_state(self):
        return self.off


class Output(Module):

    def broadcast(self, *args):
        pass

    def is_original_state(self):
        return True

class Conj(Module):

    def __init__(self, name, outputs):
        super().__init__(name, outputs)
        self.memory = {}

    def broadcast(self, input, queue, origin):
        self.memory[origin] = input
        # print(f'Name: {self.name}, memory: {self.memory}')
        output = 'low'
        for value in self.memory.values():
            if value == 'low':
                output = 'high'
                break

        for module in self.outputs:
            queue.append(Pulse(output, module, self.name))

    def add_memory(self, connection):
        self.memory[connection] = 'low'

    def is_original_state(self):
        for memory in self.memory.values():
            if memory == 'high':
                return False
        return True


def push_button(modules, pulse_counter):


    queue = [Pulse('low', 'broadcaster', 'button')]

    while queue:
        # print(queue)
        new_queue = []
        for front in queue:
            # print(front)
            front.process_pulse(modules, new_queue)
            pulse_counter[front.type] += 1
        queue = new_queue

    return None

def push_button_b(modules, pulse_counter):
    # dh 3877, qd 4001, bb 3907, dp 4027

    check = 'dp'
    queue = [Pulse('low', 'broadcaster', 'button')]
    rx_pushed = False

    while queue:
        # print(queue)
        new_queue = []
        for front in queue:
            # print(front)
            front.process_pulse(modules, new_queue)
            pulse_counter[front.type] += 1
            if front.destination == check and front.type == 'low':
                print(check + ' low signal')
                rx_pushed = True
        queue = new_queue

    # return True if rx_pushed == 1 else False

    return rx_pushed

def modules_are_original_state(modules):

    for module in modules.values():
        if not module.is_original_state():
            return False

    return True

def pulses_1000_pushes(pulse_counter, cycle_length):

    n = 1000 // cycle_length
    r = 1000 % n
    if r > 0:
        print('Incomplete cycles!!!')

    total = n ** 2

    for value in pulse_counter.values():
        total *= value


    return total

def maina(file):

    modules = {}

    with open(file, 'r') as f:
        for line in f:
            if re.match(r'broadcaster', line):
                line_split = line.strip().split(' -> ')
                name = line_split[0]
                outputs = line_split[1].split(', ')
                modules[name] = Broadcast(name, outputs)
            else:
                line_split = line.strip().split(' -> ')
                outputs = line_split[1].split(', ')
                name = line_split[0][1:]
                type = line_split[0][0]

                if type == '%':
                    modules[name] = Flfl(name, outputs)
                else:
                    modules[name] = Conj(name, outputs)

    for key, module in modules.items():
        for output in module.outputs:
            if output in modules and isinstance(modules[output], Conj):
                modules[output].add_memory(module.name)
    modules['output'] = Output('output', None)

    pulse_counter = Counter()
    cycle = 0
    while (not modules_are_original_state(modules) or cycle < 1) and cycle < 1000:
        print(cycle)
        push_button(modules, pulse_counter)
        cycle += 1

    return pulses_1000_pushes(pulse_counter, cycle)

def mainb(file):
    # rx is sent to from rm
    # rm si sent to by: dh, qd, bb, dp
    # rm sends low if receives high from dh, qd, bb, dp
    # dh, qd, bb, dp send high if they receive a low
    modules = {}

    with open(file, 'r') as f:
        for line in f:
            if re.match(r'broadcaster', line):
                line_split = line.strip().split(' -> ')
                name = line_split[0]
                outputs = line_split[1].split(', ')
                modules[name] = Broadcast(name, outputs)
            else:
                line_split = line.strip().split(' -> ')
                outputs = line_split[1].split(', ')
                name = line_split[0][1:]
                type = line_split[0][0]

                if type == '%':
                    modules[name] = Flfl(name, outputs)
                else:
                    modules[name] = Conj(name, outputs)

    for key, module in modules.items():
        for output in module.outputs:
            if output in modules and isinstance(modules[output], Conj):
                modules[output].add_memory(module.name)
    modules['output'] = Output('output', None)

    pulse_counter = Counter()
    cycle = 0
    rx_pushed_once = False
    while not rx_pushed_once and cycle < 10000000:
        # print(cycle)
        rx_pushed_once = push_button_b(modules, pulse_counter)
        cycle += 1

    return cycle


if __name__ == '__main__':

    file = './data.txt'
    # print(mainb(file))

    print(3877 * 4001 * 3907 * 4027)