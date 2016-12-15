def split_data_set(file_address, training_ratio=0.7):
    file_data_set = open(file_address)

    data_set = list()

    for line in file_data_set:
        data_set.append(line)
    file_data_set.close()

    mark = int(len(data_set)*training_ratio)
    training = data_set[:mark]
    testing = data_set[mark:]

    return training, testing


def save_data(file_name, data):
    a_file = open(file_name, 'w')
    for item in data:
        a_file.write("%s" % item)

if __name__ == '__main__':
    address = 'dataset/gate_twitter_bootstrap_corpus.1543K.tokens'
    training, testing = split_data_set(address)

    print ('training', len(training))
    print ('testing', len(testing))

    save_data('dataset/training.txt', training)
    save_data('dataset/testing.txt', testing)
