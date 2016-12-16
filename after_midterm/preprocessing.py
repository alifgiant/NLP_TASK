import re
import res
from collections import Counter


def normalize_twitter_word(word):
    if not res.is_ascii(word):
        return res.TwitterWord.SYMBOL
    elif re.match('Http://|\*\*Http://|http://|\**http://', word) is not None:
        return res.TwitterWord.URL
    elif re.match('#|\*\*#', word) is not None:
        return res.TwitterWord.HT
    elif re.match('@|\*\*@', word) is not None:
        return res.TwitterWord.USER
    else:
        return word


def normalize_low_freq(word):
    result = re.search('[0-9]+', word)
    if result is not None:
        if re.search('[a-zA-Z]+', word) is not None:
            return res.LowFrequency.ContainsDigitAndAlpha
        elif re.search('[-]+', word) is not None:
            return res.LowFrequency.ContainsDigitAndDash
        elif re.search('[/]+', word) is not None:
            return res.LowFrequency.ContainsDigitAndSlash
        elif re.search('[,]+', word) is not None:
            return res.LowFrequency.ContainsDigitAndComma
        elif re.search('[.]+', word) is not None:
            return res.LowFrequency.ContainsDigitAndPeriod
        elif len(word) == 2:
            return res.LowFrequency.TwoDigitNum
        elif len(word) == 4:
            return res.LowFrequency.FourDigitNum
        else:
            return res.LowFrequency.OtherNum
    result = re.search('[A-Z]+', word)
    if result is not None:
        if re.search('[.]+', word) is not None:
            return res.LowFrequency.CapPeriod
        elif result.group(0) == word:
            return res.LowFrequency.AllCaps
        elif word[:2] == '**':
            return res.LowFrequency.FirstWord
        elif result.group(0) == word[0]:
            return res.LowFrequency.InitCap
        else:
            return res.LowFrequency.OtherCap
    elif re.search('[a-z]+', word) is not None:
        return res.LowFrequency.Lowercase
    else:
        return res.LowFrequency.Other


def do_pre_processing(training_data, dataset_type):
    # 1. get all words and tags
    sentence_raw = list()
    tags_raw = list()

    tag_counter = Counter()  # tag token counter
    word_counter = Counter()  # word token counter

    # 2. smoothing tags count
    for tag in res.PTB_POS_TAGS:
        tag_counter[tag] += 1

    # 3. count tags appearance and split word and tags
    for line in training_data:
        terms = line.split(' ')
        sentence = []
        tags = []
        for term in terms:
            temp = term.split('_')
            tag = str(temp[-1])
            word = '_'.join(map(str, temp[:-1]))

            word = normalize_twitter_word(word)  # normalize twitter word

            tag_counter[tag] += 1  # count tag
            word_counter[word] += 1  # count word

            sentence.append(word)
            tags.append(tag)

        sentence = ' '.join(sentence)
        tags = ' '.join(tags)
        sentence_raw.append(sentence)
        tags_raw.append(tags)

    # 4. Normalize sentences
    sentence_normalize = list()
    word_normalize_counter = Counter()  # word token normalize counter
    for sentence in sentence_raw:
        splits = sentence.split(' ')
        normalized = list()
        for word in splits:
            if word_counter[word] < 5:
                if word == splits[0]:
                    word = '**' + word
                word = normalize_low_freq(word)  # normalize low freq
            normalized.append(word)
            word_normalize_counter[word] += 1
        normalized = ' '.join(normalized)
        sentence_normalize.append(normalized)
        # break

    # print sentence_normalize

    # res.re_dump_processed('dataset/rejoined_training.txt', sentence_normalize, tags_raw)
    # res.save_data('dataset/token_training.txt', word_normalize_counter.keys(), end_flag=False)
    # res.re_dump_processed('dataset/rejoined_testing.txt', sentence_normalize, tags_raw)
    # res.save_data('dataset/token_testing.txt', word_normalize_counter.keys(), end_flag=False)
    # print (word_normalize_counter.keys())

    # 5. save sentence normalized
    res.save_data(dataset_type[res.PREPROCESSED_SENTENCE], sentence_normalize, end_flag=False)
    res.save_data(dataset_type[res.PREPROCESSED_TAGS], tags_raw, end_flag=False)
    res.save_data(dataset_type[res.TAG_TOKENS], [tag+' '+str(tag_counter[tag]) for tag in tag_counter], end_flag=False)


if __name__ == '__main__':
    # print (normalize_low_freq('90/'))
    word = 'Http://www.google.com'
    # result = re.search('[A-Z]+', word)
    # if result.group(0) == word:
    res = re.search('http://|Http://', word)
    print (res is None)
    print (res.group(0))

