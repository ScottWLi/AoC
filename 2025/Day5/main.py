from utils.utils import read_file, Grid, Coordinate, DIRECTIONS
from collections import Counter
from utils.logging import logger
from bisect import bisect_left

def main1_impl(tuple_):
    idx = tuple_.index((''),)

    logger.debug(idx)

    ranges = [list(map(int, range.split('-'))) for range in tuple_[:idx]]
    ids = map(int, tuple_[idx+1:])

    total = 0
    for id in ids:
        for range in ranges:
            if id >= range[0] and id <= range[1]:
                total += 1
                break

    return total


def main2_impl(tuple_):
    idx = tuple_.index((''), )

    logger.debug(idx)

    ranges = [list(map(int, range.split('-'))) for range in tuple_[:idx]]
    ids = map(int, tuple_[idx + 1 :])

    sorted_ranges = []
    for range_list in ranges:
        if not sorted_ranges:
            sorted_ranges.append(range_list)
        elif range_list[0] < sorted_ranges[0][0] and range_list[1] > sorted_ranges[-1][1]:
            # Swallow whole list of ranges
            sorted_ranges = [range_list]
        elif range_list[0] > sorted_ranges[-1][0]:
            # no overlap with ranges - after
            sorted_ranges.append(range_list)
        elif range_list[1] < sorted_ranges[0][0]:
            # no overlap with ranges - before
            sorted_ranges.insert(0, range_list)
        elif range_list[0] < sorted_ranges[0][0]:
            # find range for which this end range inserts into
            second_insertion = bisect_left(sorted_ranges,
                                           range_list[1],
                                           key=lambda x : x[1])

            if range_list[1] < sorted_ranges[second_insertion][0]:
                second_insertion -= 1

            end_point = max(sorted_ranges[second_insertion][1], range_list[1])
            logger.debug("Overlapping start")
            logger.debug("%s", range_list)
            logger.debug("%s contains %s", [range_list[0], end_point], sorted_ranges[:second_insertion+1])
            del sorted_ranges[:second_insertion+1]
            sorted_ranges.insert(0, [range_list[0], end_point])
        elif range_list[1] > sorted_ranges[-1][1]:
            insertion = bisect_left(sorted_ranges,
                                    range_list[0],
                                    key=lambda x: x[0])

            if range_list[0] <= sorted_ranges[insertion-1][1]:
                insertion -= 1
            start_point = min(range_list[0], sorted_ranges[insertion][0])
            logger.debug("Overlapping end")
            logger.debug("%s", range_list)
            logger.debug("%s contains %s", [start_point, range_list[1]], sorted_ranges[insertion:])
            del sorted_ranges[insertion:]
            sorted_ranges.append([start_point, range_list[1]])
        else:
            # range starts after the start of first element and ends before end of last element

            # find where range_list[0] inserts into (based on lefts)
            # check idx-1 right - start is idx-1 left or range_list[0]

            # find where range_list[1] inserts into (based on rights)
            # check idx left - right-most is idx right or range_list[0]

            # work out which ones to delete

            insertion = bisect_left(sorted_ranges,
                                    range_list[0],
                                    key=lambda x: x[0])
            second_insertion = bisect_left(sorted_ranges,
                                           range_list[1],
                                           key=lambda x : x[1])


            if range_list[1] < sorted_ranges[second_insertion][0]:
                second_insertion -= 1
            end_point = max(sorted_ranges[second_insertion][1], range_list[1])

            if range_list[0] <= sorted_ranges[insertion-1][1]:
                insertion -= 1
            start_point = min(range_list[0], sorted_ranges[insertion][0])

            logger.debug("%s", range_list)
            logger.debug("%s contains %s", [start_point, end_point], sorted_ranges[insertion:second_insertion+1])
            del sorted_ranges[insertion:second_insertion+1]
            sorted_ranges.insert(insertion, [start_point, end_point])

    logger.debug(sorted_ranges)

    total = 0
    for range in sorted_ranges:
        total += range[1] - range[0] + 1

    return total

# 344813017450469
#

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
