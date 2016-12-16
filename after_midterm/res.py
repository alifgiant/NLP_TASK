RAW = 'raw'
TAG_TOKENS = 'tag_token'
PREPROCESSED_SENTENCE = 'sentence'
PREPROCESSED_TAGS = 'tags'
EMISSION_CPT = 'emision'
TRANSITION_UNIGRAM = 'unigram'
TRANSITION_BIGRAM = 'bigram'
TRANSITION_TRIGRAM = 'trigram'


class DataSet(object):
    Training = {RAW: 'dataset/training.txt',
                TAG_TOKENS: 'dataset/training_tag_tokens.txt',
                PREPROCESSED_SENTENCE: 'dataset/training_sentence.txt',
                PREPROCESSED_TAGS: 'dataset/training_tags.txt',
                EMISSION_CPT: 'dataset/training_emission_cpt.txt',
                TRANSITION_UNIGRAM: 'dataset/training_transition_unigram_cpt.txt',
                TRANSITION_BIGRAM: 'dataset/training_transition_bigram_cpt.txt',
                TRANSITION_TRIGRAM: 'dataset/training_transition_trigram_cpt.txt'}
    Testing = {RAW: 'dataset/testing.txt',
               TAG_TOKENS: 'dataset/testing_tag_tokens.txt',
               PREPROCESSED_SENTENCE: 'dataset/testing_sentence.txt',
               PREPROCESSED_TAGS: 'dataset/testing_tags.txt',
               EMISSION_CPT: 'dataset/testing_emission_cpt.txt',
               TRANSITION_UNIGRAM: 'dataset/testing_transition_unigram_cpt.txt',
               TRANSITION_BIGRAM: 'dataset/testing_transition_bigram_cpt.txt',
               TRANSITION_TRIGRAM: 'dataset/testing_transition_trigram_cpt.txt'}


PTB_POS_TAGS = [
    '$',
    '``',
    '\'\'',
    '(',
    ')',
    ',',
    '--',
    '.',
    ':',
    'CC',
    'CD',
    'DT',
    'EX',
    'FW',
    'IN',
    'JJ',
    'JJR',
    'JJS',
    'LS',
    'MD',
    'NN',
    'NNP',
    'NNPS',
    'NNS',
    'PDT',
    'POS',
    'PRP',
    'PRP$',
    'RB',
    'RBR',
    'RBS',
    'RP',
    'SYM',
    'TO',
    'UH',
    'VB',
    'VBD',
    'VBG',
    'VBN',
    'VBP',
    'VBZ',
    'WDT',
    'WP',
    'WP$',
    'WRB',
    'USR',
    'HT',
    'RT',
    'URL',
]  # http://www.comp.leeds.ac.uk/ccalas/tagsets/upenn.html


# Bikel et. al 1999, named entity recognition, +OtherCap (LoL, aWWk)
class LowFrequency(object):
    TwoDigitNum = '[twoDigitNum]'
    FourDigitNum = '[fourDigitNum]'
    ContainsDigitAndAlpha = '[containsDigitAndAlpha]'
    ContainsDigitAndDash = '[containsDigitAndDash]'
    ContainsDigitAndSlash = '[containsDigitAndSlash]'
    ContainsDigitAndComma = '[containsDigitAndComma]'
    ContainsDigitAndPeriod = '[containsDigitAndPeriod]'
    OtherNum = '[otherNum]'
    AllCaps = '[allCaps]'
    CapPeriod = '[capPeriod]'
    FirstWord = '[firstWord]'
    InitCap = '[initCap]'
    Lowercase = '[lowercase]'
    Other = '[other]'
    OtherCap = '[otherCap]'


class TwitterWord(object):
    URL = '[http]'
    HT = '[hashtag]'
    USER = '[user]'
    SYMBOL = '[symbol]'


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


def load_data(data_set_type, quality=RAW):
    the_file = open(data_set_type[quality])
    data_set = list()
    for line in the_file:
        data_set.append(line[:-1])
    return data_set


def load_data_with_split(data_set_type, quality=RAW, split_char=' '):
    the_file = open(data_set_type[quality])
    data_set = list()
    for line in the_file:
        line = line[:-1].split(split_char)
        data_set.append(line)
    return data_set

if __name__ == '__main__':
    address = 'dataset/gate_twitter_bootstrap_corpus.1543K.tokens'
    training, testing = __split_data_set(address)

    print ('training', len(training))
    print ('testing', len(testing))

    save_data(DataSet.Training['address'], training, end_flag=True)
    save_data(DataSet.Testing['address'], testing, end_flag=True)
