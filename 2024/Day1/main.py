from utils.utils import read_file
from collections import Counter

def main1_impl(tuple):

    split_data = (_str.split() for _str in tuple)

    left_list, right_list = zip(*(map(int, pair) for pair in split_data))

    left_list = sorted(left_list)
    right_list = sorted(right_list)

    total = 0

    for left_item, right_item in zip(left_list, right_list):
        total += abs(left_item - right_item)

    return total

def main2_impl(tuple):
    split_data = (_str.split() for _str in tuple)

    left_list, right_list = zip(*(map(int, pair) for pair in split_data))

    left_counter = Counter(left_list)
    right_counter = Counter(right_list)

    total = 0
    for key, value in left_counter.items():
        total += key * value * right_counter[key]

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
