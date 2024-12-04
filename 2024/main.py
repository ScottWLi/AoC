from pathlib import PurePath
from Day3.main import main1, main2

if __name__ == '__main__':
    day = 3

    example = 'example2.txt'
    data = 'data.txt'

    example_path = PurePath(f'Day{day}', example)
    data_path = PurePath(f'Day{day}', data)

    print(main2(data_path))