import re
from collections import Counter

PATTERN = r"\s+(\d+)"

def decipher_line(str):

    colon_split = str.split(':')

    game_id = int(re.findall(PATTERN, colon_split[0])[0])

    winning_numbers, current_numbers = colon_split[1].split('|')

    winning_numbers = set([int(i) for i in re.findall(PATTERN, winning_numbers)])
    current_numbers = set([int(i) for i in re.findall(PATTERN, current_numbers)])

    return game_id, len(winning_numbers.intersection(current_numbers))

def maina(file):

    sum = 0

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            game_id, n_games = decipher_line(line)
            print(game_id, n_games)
            if n_games > 0:
                sum += 2**(n_games-1)
    return sum

def mainb(file):

    sum = 0
    extras = Counter()

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            game_id, n_games = decipher_line(line)
            print(game_id, n_games)

            if n_games > 0:
                for i in range(n_games):
                    extras[game_id + i + 1] += (1 + extras[game_id])

            sum += (extras[game_id] + 1)

    return sum


if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))