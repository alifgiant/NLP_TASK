class DataSet(object):
    Training = {'address': 'dataset/training.txt'}
    Testing = {'address': 'dataset/testing.txt'}


def is_ascii(text):
    if isinstance(text, unicode):
        try:
            text.encode('ascii')
        except UnicodeEncodeError:
            return False
    else:
        try:
            text.decode('ascii')
        except UnicodeDecodeError:
            return False
    return True


def __split_data_set(file_address, training_ratio=0.7):
    file_data_set = open(file_address)

    data_set = list()

    for line in file_data_set:
        data_set.append(line)
    file_data_set.close()

    mark = int(len(data_set)*training_ratio)
    training = data_set[:mark]
    testing = data_set[mark:]

    return training, testing


def save_data(file_name, data, end_flag=False):
    a_file = open(file_name, 'w')
    for item in data:
        if end_flag:
            item = item[:-1]
        a_file.write("%s\n" % item)


def re_dump_processed(address, sentences, tags_chain):
    sentences_rejoined = list()
    for sentence, tags in zip(sentences, tags_chain):
        split_sentence = sentence.split(' ')
        split_tags = tags.split(' ')
        rejoined = list()
        for word, tag in zip(split_sentence, split_tags):
            rejoined.append(word+'_'+tag)
        rejoined = ' '.join(rejoined)
        sentences_rejoined.append(rejoined)
    save_data(address, sentences_rejoined)


def load_data(data_type):
    the_file = open(data_type['address'])
    data_set = list()
    for line in the_file:
        data_set.append(line[:-1])
    return data_set

if __name__ == '__main__':
    address = 'dataset/gate_twitter_bootstrap_corpus.1543K.tokens'
    training, testing = __split_data_set(address)

    print ('training', len(training))
    print ('testing', len(testing))

    save_data(DataSet.Training['address'], training, end_flag=True)
    save_data(DataSet.Testing['address'], testing, end_flag=True)
