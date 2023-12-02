from collections import Counter

N_RED = 12
N_GREEN = 13
N_BLUE = 14

max_balls = {
    'red':N_RED,
    'green':N_GREEN,
    'blue':N_BLUE
}

def decipher_line(str):

    colon_split = str.split(':')

    game_id = int(colon_split[0].split(' ')[1])
    games_string_list = colon_split[1].split(';')

    games_proc_list = []

    for game in games_string_list:

        balls_list = game.split(',')

        balls_count_list = []

        for ball_set in balls_list:
            ball_set_split = ball_set.split(' ')
            balls_count_list.append(tuple(ball_set_split[1:]))

        games_proc_list.append(tuple(balls_count_list))

    return game_id, games_proc_list

def satisfies_balls(n, color):

    if int(n) > max_balls[color]:
        return False

    return True

def maina(file):

    value = 0

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            valid_game = True
            game_id, games_proc_list = decipher_line(line)

            for game in games_proc_list:
                for n, color in game:
                    if not satisfies_balls(n, color):
                        valid_game = False
                        break

                if not valid_game:
                    break
            if valid_game:
                value += game_id

    return value

def mainb(file):

    sum_powers = 0

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            game_id, games_proc_list = decipher_line(line)

            tracker = Counter({'red': 0, 'blue':0, 'green':0})

            for game in games_proc_list:
                for n, color in game:

                    tracker[color] = max(tracker[color], int(n))

            power = 1
            for _, value in tracker.items():

                power *= value

            print(f'{line}, has tracker {tracker} with power {power}')

            sum_powers += power

    return sum_powers

if __name__ == '__main__':

    file = './data.txt'
    print(mainb(file))