VALID_SYMBOLS = set("!@#$%^&*()_-+={}[]")
DIRECTIONS = [(0, -1), (0, 1)]

def input_code_as_grid(file):
    grid = []

    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            grid.append(line)

    return grid

def main(file):

    sum = 0

    found_parts = {}
    in_a_run = False
    near_engine_part = False
    current_part = None
    running_digits = ''

    grid = input_code_as_grid(file)
    m = len(grid)
    n = len(grid[0])

    # Row is specified with i, column is specified with j
    # x is column index, y is row index

    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char.isnumeric():
                if in_a_run:
                    running_digits += char
                    for dj, di in [(0, -1), (0, 1)]:
                        nj, ni = j + dj, i + di
                        if (nj >= 0) and (nj < n) and (ni >= 0) and (ni < m) and not grid[ni][nj].isnumeric() and grid[ni][nj] != ".":
                            near_engine_part = True
                            current_part = (ni, nj)
                else:
                    in_a_run = True
                    running_digits = char
                    for dj, di in [(0, -1), (0, 1), (-1, -1), (-1, 0), (-1, 1)]:
                        nj, ni = j + dj, i + di
                        if (nj >= 0) and (nj < n) and (ni >= 0) and (ni < m) and not grid[ni][nj].isnumeric() and grid[ni][nj] != ".":
                            near_engine_part = True
                            current_part = (ni, nj)
            else:
                if in_a_run:
                    for dj, di in [(0, -1), (0, 0), (0, 1)]:
                        nj, ni = j + dj, i + di
                        if (nj >= 0) and (nj < n) and (ni >= 0) and (ni < m) and not grid[ni][nj].isnumeric() and grid[ni][nj] != ".":
                            near_engine_part = True
                            current_part = (ni, nj)
                    if near_engine_part:
                        if current_part not in found_parts:
                            found_parts[current_part] = int(running_digits)
                        else:
                            sum += int(running_digits) * found_parts[current_part]
                        print(f'{running_digits} Found when not at end of a row')

                    in_a_run = False
                    running_digits = ''
                    near_engine_part = False
                    current_part = None

        if near_engine_part:
            if current_part not in found_parts:
                found_parts[current_part] = int(running_digits)
            else:
                sum += int(running_digits) * found_parts[current_part]
            print(f'{running_digits} Found when at end of a row')

        in_a_run = False
        running_digits = ''
        near_engine_part = False
        current_part = None

    return sum

if __name__ == '__main__':

    file = './data.txt'
    print(main(file))