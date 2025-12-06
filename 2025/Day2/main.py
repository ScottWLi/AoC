from utils.utils import read_file
from collections import Counter
from utils.logging import logger

def is_invalid(str_, chunks=2):
    length = len(str_)
    if length % chunks != 0:
        return False

    n = length // chunks

    chunks = [str_[i :i + n] for i in range(len(str_)) if i % n == 0]

    return len(set(chunks)) == 1

def main1_impl(tuple_):
    all_pairs = tuple_[0].split(',')

    total = 0
    for pairs in all_pairs:
        start, end = pairs.split('-')
        for val in range(int(start), int(end)+1):
            val_str = str(val)
            if is_invalid(val_str, 2):
                logger.debug(f"Invalid id: {val_str}")
                total += int(val_str)

    return total

def main2_impl(tuple_):
    all_pairs = tuple_[0].split(',')

    total = 0
    for pairs in all_pairs:
        start, end = pairs.split('-')
        for val in range(int(start), int(end)+1):
            val_str = str(val)
            length = len(val_str)
            for chunks in range(2, length+1):
                if is_invalid(val_str, chunks):
                    logger.debug(f"Invalid id: {val_str}")
                    total += int(val_str)
                    break

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
