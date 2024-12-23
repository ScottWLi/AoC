from pathlib import PurePath
from Day21.main import main1, main2, count_sequence

if __name__ == '__main__':
    day = 21

    example = 'example.txt'
    example2 = 'example2.txt'
    data = 'data.txt'

    example_path = PurePath(f'Day{day}', example)
    example2_path = PurePath(f'Day{day}', example2)
    data_path = PurePath(f'Day{day}', data)

    print(main2(data_path))

