import time
import numpy as np

# region pre processing
from collections import Counter
import res
import preprocessing
# 1. load training data
start_pre_processing = time.time()
training_data = res.load_data(res.DataSet.Training)
# training_data = res.load_data(res.DataSet.Testing)

# 2. get all words and tags
sentence_raw = list()
tags_raw = list()

tag_counter = Counter()  # tag token counter
word_counter = Counter()  # word token counter

# 3. smoothing tags count
for tag in preprocessing.PTB_POS_TAGS:
    tag_counter[tag] += 1

# 4. count tags appearance and split word and tags
for line in training_data:
    terms = line.split(' ')
    sentence = []
    tags = []
    for term in terms:
        temp = term.split('_')
        tag = str(temp[-1])
        word = '_'.join(map(str, temp[:-1]))

        word = preprocessing.normalize_twitter_word(word)  # normalize twitter word

        tag_counter[tag] += 1  # count tag
        word_counter[word] += 1  # count word

        sentence.append(word)
        tags.append(tag)

    sentence = ' '.join(sentence)
    tags = ' '.join(tags)
    sentence_raw.append(sentence)
    tags_raw.append(tags)

# 5. Normalize sentences
sentence_normalize = list()
word_normalize_counter = Counter()  # word token normalize counter
for sentence in sentence_raw:
    splits = sentence.split(' ')
    normalized = list()
    for word in splits:
        temp = preprocessing.normalize_low_freq(word)
        if word_counter[word] < 5:
            word = temp
        normalized.append(word)
        word_normalize_counter[word] += 1
    normalized = ' '.join(normalized)
    sentence_normalize.append(normalized)
    # break

# print sentence_normalize

# res.re_dump_processed('dataset/rejoined_training.txt', sentence_normalize, tags_raw)
res.save_data('dataset/token_training.txt', word_normalize_counter.keys(), end_flag=False)
# res.re_dump_processed('dataset/rejoined_testing.txt', sentence_normalize, tags_raw)
# res.save_data('dataset/token_testing.txt', word_normalize_counter.keys(), end_flag=False)
# print (word_normalize_counter.keys())


stop_pre_processing = time.time()
print ('execution pre processing:', stop_pre_processing-start_pre_processing)
# endregion
