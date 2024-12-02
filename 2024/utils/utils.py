def read_file(file_path):
    with open(file_path, 'r') as f:
        data = tuple(line.strip() for line in f)

    return data