from utils.utils import read_file
from collections import Counter

def report_is_safe(_tuple):
    difference = tuple(a - b for a, b in zip(_tuple[1:], _tuple[:-1]))

    sign = difference[0] > 0

    for elem in difference:
        sign_new = elem > 0

        if sign_new != sign or abs(elem) > 3 or not elem:
            return False

    return True

def main1_impl(tuple_):

    split_data = (_str.split() for _str in tuple_)

    reports = tuple(tuple(map(int, _tuple)) for _tuple in split_data)

    total = 0

    for report in reports:
        if report_is_safe(report):
            total += 1

    return total

def main2_impl(tuple_):

    split_data = (_str.split() for _str in tuple_)

    reports = tuple(tuple(map(int, _tuple)) for _tuple in split_data)

    total = 0

    for report in reports:
        if report_is_safe(report):
            total += 1
            continue
        else:
            for idx in range(len(report)):
                copy = report[:idx] + report[idx+1:]
                if report_is_safe(copy):
                    total += 1
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
