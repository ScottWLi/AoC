from utils.utils import read_file
from collections import Counter
from utils.logging import logger

def biggest_joltage(str_) -> tuple[int, int]:
    if len(str_) == 2:
        return int(str_), max(int(str_[0]), int(str_[1]))

    first = str_[0]
    last = str_[1:]

    largest_joltage, biggest_number = biggest_joltage(last)

    largest_joltage = max(int(first + str(biggest_number)), largest_joltage)
    biggest_number = max(int(first), biggest_number)

    return largest_joltage, biggest_number


# take left if larger than left-most, then left-squash
#
def left_squash(str_):
    prev = int(str_[0])
    for i in range(1, len(str_)):
        current = int(str_[i])
        if current > prev:
            #remove i-1'th element
            return str_[:i-1] + str_[i:]

        prev = current

    return str_[:-1]

def biggest_joltage_n(str_, n) -> int:
    if len(str_) == n:
        return int(str_)

    first = str_[0]
    last = str_[1:]

    largest_joltage = biggest_joltage_n(last, n)

    largest_joltage_str = str(largest_joltage)

    if int(first) >= int(largest_joltage_str[0]):
        return int(first + left_squash(largest_joltage_str))

    return largest_joltage




def main1_impl(tuple_):
    total = 0
    for row in tuple_:
        largest_joltage = biggest_joltage_n(row, 2)
        total += largest_joltage

    return total

def main2_impl(tuple_):
    total = 0
    for row in tuple_:
        largest_joltage = biggest_joltage_n(row, 12)
        total += largest_joltage

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
