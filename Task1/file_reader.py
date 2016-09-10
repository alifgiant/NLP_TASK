def get_target(file_path):
    file_text = open(file_path)

    target = list()
    for line in file_text:
        if line != '\n':
            target += line.split('\n')
    # print target
    return target
