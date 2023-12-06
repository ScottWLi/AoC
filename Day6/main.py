import re
from collections import Counter
import math

PATTERN = r"\s+(\d+)"

def time_distances_from_input(file):

    with open(file, 'r') as f:

        line = f.readline()
        time_list = [int(i) for i in re.findall(PATTERN, line)]

        line = f.readline()
        distance_list = [int(i) for i in re.findall(PATTERN, line)]

        zipped_list = []

        for time, distance in zip(time_list, distance_list):
            zipped_list.append((time, distance))

    return zipped_list

def ways_to_beat_record(tuple):
    # Speed is time_charged
    # (record - time_charged * time_charged) > distance
    # x is time_charged
    # (tx - x^2) > d
    # x^2 - tx + d < 0
    # x = t +- sqrt(t^2 -4d) / 2

    t = tuple[0]
    d = tuple[1]

    x_start = (t - (t**2 - 4 * d)**0.5) / 2
    x_end = (t + (t**2 - 4 * d)**0.5) / 2

    if x_end.is_integer():
        x_end = int(x_end) - 1
    else:
        x_end = int(math.floor(x_end))

    if x_start.is_integer():
        x_start = int(x_start) + 1
    else:
        x_start = int(math.ceil(x_start))

    print(f'From {x_start} to {x_end} with {x_end - x_start + 1} combinations')

    return x_end - x_start + 1

def maina(file):

    product = 1
    time_distance_list = time_distances_from_input(file)

    for tuple in time_distance_list:
        product *= ways_to_beat_record(tuple)

    return product

def time_distances_from_input_b(file):

    with open(file, 'r') as f:

        line = f.readline()
        time_list = ''.join(re.findall(PATTERN, line))

        line = f.readline()
        distance_list = ''.join(re.findall(PATTERN, line))

    return (int(time_list), int(distance_list))

def mainb(file):

    time_distance_tuple = time_distances_from_input_b(file)

    return ways_to_beat_record(time_distance_tuple)


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))