import re
from collections import Counter


def clean(source):
    print 'cleaning'
    # region CLEANING
    criteria_cleaning = ''
    # 1. hapus meta script
    criteria_cleaning += '<.*>'
    # 2. hapus parentheses
    criteria_cleaning += '|\(.*\)'
    # 3. hapus digit dan titik antara digit
    criteria_cleaning += '|[0-9]+[\.*0-9]*'
    # 4. hapus semua simbol selain titik
    criteria_cleaning += '|[^a-zA-Z\. \n]'

    regex = re.compile(criteria_cleaning)
    subs = regex.sub('', source)

    # 5. hapus space yang tidak perlu
    # 5.1 ganti enter berlebih jadi .
    criteria_cleaning = '\n+'
    regex = re.compile(criteria_cleaning, re.MULTILINE)
    subs = regex.sub(' ', subs)

    # 5.2 ganti spasi berlebih jadi satu spasi
    criteria_cleaning = ' {2,}'
    regex = re.compile(criteria_cleaning)
    subs = regex.sub(' ', subs)

    # 5.3 ganti . berlebih jadi satu .
    criteria_cleaning = '\.{2,}'
    regex = re.compile(criteria_cleaning)
    subs = regex.sub('.', subs)

    # print subs

    return subs
    # endregion


def normalizing(cleaned):
    print 'normalizing'
    # region NORMALIZING
    # 1. split by '.'
    split_dot = cleaned.split('.')
    # 2. add <s> diawal dan </s> diakhir, 3. kecilkan semua huruf
    normalized = ['<s>'+sentence.lower()+' </s>' for sentence in split_dot if len(sentence) > 0 and sentence != ' ']
    return normalized
    # endregion


def get_unigram_n_bigram(sentences):
    # region unigram and bigram model
    bag_of_words = Counter()
    for line in sentences:
        print 'proc unigram', line[5]
        words = line.split(' ')
        bag_of_words += Counter(words)

    total_words = sum(bag_of_words.values())
    # print total_words

    unigram = {}
    for word in bag_of_words:
        unigram[word] = float(bag_of_words[word]) / total_words

    paired_bag_of_words = {}
    for line in sentences:
        print 'proc bigram', line[5]
        words = line.split(' ')
        for i in range(len(words))[1:]:
            if words[i] not in paired_bag_of_words:
                paired_bag_of_words[words[i]] = Counter()
            paired_bag_of_words[words[i]][words[i - 1]] += 1

    bigram = {}
    for word in paired_bag_of_words:
        bigram[word] = {}
        for preceded_by in paired_bag_of_words[word]:
            bigram[word][preceded_by] = float(paired_bag_of_words[word][preceded_by]) / bag_of_words[preceded_by]

    return bag_of_words, paired_bag_of_words, unigram, bigram
    # endregion

