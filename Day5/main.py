import re
from collections import Counter

PATTERN = r"\s*(\d+)"

def update_seeds_with_mapping_list(seed_list, mapping_list):

    for i, val in enumerate(seed_list):
        for mapping_tuple in mapping_list:
            if val >= mapping_tuple[1] and val < (mapping_tuple[1] + mapping_tuple[2]):
                seed_list[i] = mapping_tuple[0] + (val - mapping_tuple[1])
                break

    return seed_list

def maina(file):

    sum = 0

    with open(file, 'r') as f:

        seeds_line = f.readline()
        print(seeds_line)
        colon_split = seeds_line.split(':')
        seeds_list = [int(i) for i in re.findall(PATTERN, colon_split[1])]
        f.readline()

        mapping_list = []
        for line in f:
            if line == "\n":
                seed_list = update_seeds_with_mapping_list(seeds_list, mapping_list)
                mapping_list = []
            elif line[0].isnumeric():
                mapping_list.append(tuple([int(i) for i in re.findall(PATTERN, line)]))

    return seed_list

def mainb(file):

    sum = 0

    with open(file, 'r') as f:

        mapping_list_list = []
        mapping_list = []

        seed_list = []

        for line in f:
            if line == "\n":
                mapping_list_list.append(mapping_list)
                mapping_list = []
            elif line[0].isnumeric():
                mapping_list.append(tuple([int(i) for i in re.findall(PATTERN, line)]))
            elif line[0:6] == "seeds:":
                temp_list = [int(i) for i in re.findall(PATTERN, line[7:])]
                for i in range(len(temp_list)//2):
                    seed_list.append(tuple(temp_list[i*2:(i+1)*2]))

    for i in range(218000000, 1000000000):
        val = i
        for mapping_list in mapping_list_list:
            val = update_seeds_with_mapping_list_b(val, mapping_list)

        if val_in_seed_list(val, seed_list):
            return val

        if (i // 1000000) * 1000000 == i:
            print(i)

    return -1

def mainbb(file):

    sum = 0

    with open(file, 'r') as f:

        seeds_line = f.readline()
        print(seeds_line)
        seeds_list = [int(i) for i in re.findall(PATTERN, seeds_line[7:])]

        seed_range_list = []

        for i in range(len(seeds_list) // 2):
            seed_range_list.append(tuple(seeds_list[i * 2:(i + 1) * 2]))

        f.readline()


        mapping_list = []
        for line in f:
            if line == "\n":
                # print('Before:')
                # print(seed_range_list, mapping_list)
                seed_range_list = update_seed_range_list_with_mapping_list(seed_range_list, mapping_list)
                # print('After:')
                print(len(seed_range_list))
                mapping_list = []
            elif line[0].isnumeric():
                mapping_list.append(tuple([int(i) for i in re.findall(PATTERN, line)]))

    minimum = None
    for seed_tuple in seed_range_list:
        if not minimum:
            minimum = seed_tuple[0]
        else:
            minimum = min(minimum, seed_tuple[0])

    return minimum

def reverse_lines_in_text_file(file):
    # inverts file line(s) and writes to a new file
    # tries to open import file in reading mode
    f1 = open(file, "r")

    # tries to create export file in write mode
    f2 = open('reversed_data.txt', "w")

    # creates a list with each line in a separate index
    line_list = f1.readlines()

    # reverses line order
    line_list.reverse()

    # closes import file, since all data is stored in line_list
    f1.close()

    # loops through line_list to modify individual indices
    for line in line_list:

        # appends the line to the new file
        f2.write(line)

    # once the loop is finished, close the new file
    f2.close()

def val_in_seed_list(val, seed_list):

    for seed_tuple in seed_list:
        if val >= seed_tuple[0] and val < (seed_tuple[0] + seed_tuple[1]):
            return True

    return False

def update_seeds_with_mapping_list_b(val, mapping_list):

    for mapping_tuple in mapping_list:
        if val >= mapping_tuple[0] and val < (mapping_tuple[0] + mapping_tuple[2]):
            seed_val = mapping_tuple[1] + (val - mapping_tuple[0])
            break

    return val

def update_seed_range_list_with_mapping_list(seed_range_list, mapping_list):

    # For a given seed range interval:
    # If the mapping overlaps the start:
    # Add the result of the overlap section to a new list
    # If the mapping is contained in the range:
    # Add the end of the mapping to the list
    # If the mapping overlaps the end:
    # add the overlap to a list
    # Else add original interval to the new list

    new_seed_range_list = []
    seed_range_list = seed_range_list.copy()

    while seed_range_list:

        need_to_add = True
        seed_range_tuple = seed_range_list.pop()

        for mapping_tuple in mapping_list:
            if seed_range_tuple[0] >= mapping_tuple[1] and seed_range_tuple[0] < (mapping_tuple[1] + mapping_tuple[2]) and (seed_range_tuple[0] + seed_range_tuple[1]) >= (mapping_tuple[1] + mapping_tuple[2]):
                # print(f'Map overlap with start: Seed range: {seed_range_tuple} and Map: {mapping_tuple}')
                new_seed_range_list.append((mapping_tuple[0] + seed_range_tuple[0] - mapping_tuple[1], -seed_range_tuple[0] + mapping_tuple[1] + mapping_tuple[2]))
                seed_range_list.append((mapping_tuple[1] + mapping_tuple[2], seed_range_tuple[0] + seed_range_tuple[1] - (mapping_tuple[1] + mapping_tuple[2])))
                need_to_add = False
                break
            elif seed_range_tuple[0] < mapping_tuple[1] and (seed_range_tuple[0] + seed_range_tuple[1]) >= (mapping_tuple[1] + mapping_tuple[2]):
                # print(f'Map is contained: Seed range: {seed_range_tuple} and Map: {mapping_tuple}')
                new_seed_range_list.append((mapping_tuple[0], mapping_tuple[2]))
                seed_range_list.append((seed_range_tuple[0], mapping_tuple[1] - seed_range_tuple[0]))
                seed_range_list.append((mapping_tuple[1]+mapping_tuple[2], seed_range_tuple[0] + seed_range_tuple[1] - (mapping_tuple[1]+mapping_tuple[2])))
                need_to_add = False
                break
            elif seed_range_tuple[0] >= mapping_tuple[1] and (seed_range_tuple[0] + seed_range_tuple[1]) < (mapping_tuple[1] + mapping_tuple[2]):
                new_seed_range_list.append((mapping_tuple[0] + seed_range_tuple[0] - mapping_tuple[1], seed_range_tuple[1]))
                need_to_add = False
                break
            elif seed_range_tuple[0] < mapping_tuple[1] and (seed_range_tuple[0] + seed_range_tuple[1]) < (mapping_tuple[1] + mapping_tuple[2]) and (seed_range_tuple[0] + seed_range_tuple[1]) > mapping_tuple[1]:
                # print(f'Map overlap with end: Seed range: {seed_range_tuple} and Map: {mapping_tuple}')
                new_seed_range_list.append((mapping_tuple[0], -mapping_tuple[1] + seed_range_tuple[0] + seed_range_tuple[1]))
                seed_range_list.append((seed_range_tuple[0], mapping_tuple[1] - seed_range_tuple[0]))
                need_to_add = False
                break
        if need_to_add:
            new_seed_range_list.append(seed_range_tuple)

    # print(f'Intermediate: {new_seed_range_list}')
    # return new_seed_range_list
    return concat_disjoint_ranges(new_seed_range_list)

def concat_disjoint_ranges(seed_range_list):
    start_range_dict = {}
    for seed_tuple in seed_range_list:
        start_range_dict[seed_tuple[0]] = seed_tuple[1]

    new_start_range_dict = {}

    for key, value in start_range_dict.items():
        if key + value in start_range_dict:
            new_start_range_dict[key] = start_range_dict[key + value] + value
        else:
            new_start_range_dict[key] = value

    new_seed_range_list = []

    for key, value in start_range_dict.items():
        new_seed_range_list.append((key, value))

    return new_seed_range_list

"""
seed to soil 82 -> 84

Before:
[(79, 14), (55, 13)] [(50, 98, 2), (52, 50, 48)]

(79, 14) => (81, 14)
(55, 13) => (57, 13)

After:
[(57, 13), (81, 14)]


# 55 -> 68 => 57 -> 70
# should return [(57, 13), (81, 14)]

soil to fertilizer 84 -> 84
# Before:
# [(55, 13), (79, 14)] [(0, 15, 37), (37, 52, 2), (39, 0, 15)]
# After:
# [(79, 14), (55, 13)]
# 

fertilizer to water 84 -> 84
Before:
[(79, 14), (55, 13)] [(49, 53, 8), (0, 11, 42), (42, 0, 7), (57, 7, 4)]

55, 6 => 51, 6 correct

61, 7 => 61, 7 correct

79, 14 => 79, 14 correct


After: 84 -> 77
[(51, 6), (61, 7), (79, 14)]

Before:
[(51, 6), (61, 7), (79, 14)] [(88, 18, 7), (18, 25, 70)]

(51, 6) => (44, 6)
(61, 7) => (54, 7)
(79, 14) -> (72, 14)

After:
[(79, 14), (61, 7), (51, 6)]

"""


if __name__ == '__main__':

    file = './data.txt'
    print(mainbb(file))
