# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

def calculate_calibration_values_a(s):

    first_num = ''
    second_num = ''

    start = 0
    end = len(s) - 1

    while end > start:
        char = s[start]
        if char.isnumeric():
            first_num = char
            break
        start += 1

    while end >= start:
        char = s[end]
        if char.isnumeric():
            second_num = char
            break
        end -= 1

    return first_num + second_num

def sum_cal_values_over_data_a(file):
    value = 0

    with open(file, 'r') as f:
        for line in f:
            value += int(calculate_calibration_values_a(line))
    # code

    return value

def calculate_calibration_values_b(s):

    first_num = ''
    second_num = ''

    start = 0
    end = len(s) - 1

    while end > start:

        if start > len(s) - 5:
            chars = s[start:]
        else:
            chars = s[start:start + 5]

        result, answer = is_spelled_out_number(chars)
        if result:
            first_num = answer
            break
        start += 1

    while end >= start:
        if end > len(s) - 5:
            chars = s[end:]
        else:
            chars = s[end:end + 5]

        result, answer = is_spelled_out_number(chars)

        if result:
            second_num = answer
            break
        end -= 1

    return first_num + second_num

def is_spelled_out_number(substring):
    #Substring is a string of at most 5 characters

    result = False
    answer = None

    spelled_out_numbers_three = {'one':'1', 'two':'2', 'six':'6'}
    spelled_out_numbers_four = {'four':'4', 'five':'5', 'nine':'9'}
    spelled_out_numbers_five = {'three':'3', 'seven':'7', 'eight':'8'}

    if len(substring) >= 5:
        if substring in spelled_out_numbers_five:
            return True, spelled_out_numbers_five[substring]
    if len(substring) >= 4:
        if substring[:4] in spelled_out_numbers_four:
            return True, spelled_out_numbers_four[substring[:4]]
    if len(substring) >= 3:
        if substring[:3] in spelled_out_numbers_three:
            return True, spelled_out_numbers_three[substring[:3]]
    if substring[0].isnumeric():
        return True, substring[0]

    return result, answer

def sum_cal_values_over_data_b(file):
    value = 0

    with open(file, 'r') as f:
        for line in f:
            print(line, calculate_calibration_values_b(line))
            value += int(calculate_calibration_values_b(line))
    # code

    return value

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file = './data.txt'
    print(sum_cal_values_over_data_b(file))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
