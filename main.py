import sys
import os
import json
import preprocessing
import analyzer

# default_text_dir = 'Task1/extracted_text_sampled.txt'
default_text_dir = 'Task1/extracted_text.txt'

bag_of_words, paired_bag_of_words, unigram, bigram = None, None, None, None
if len(sys.argv) < 2:
    if len(sys.argv) == 2:
        corpus_text = sys.argv[1]
        if os.path.isfile(corpus_text):
            source = open(corpus_text)
        else:
            print 'file not found, continuing with default', default_text_dir
            source = open(default_text_dir)
    else:
        print 'opening default corpus'
        source = open(default_text_dir)

    # 1. Cleaning
    cleaned = preprocessing.clean(source.read())
    source.close()

    # 2. Normalizing
    normalized = preprocessing.normalizing(cleaned)

    # 3. calculate unigram and bigram
    # learning = normalized[:len(normalized)-10]  # sampled to last 10
    learning = normalized
    testing = normalized[-10:]  # last 10 is for testing

    # bag_of_words, paired_bag_of_words, unigram, bigram
    result_data = preprocessing.get_unigram_n_bigram(learning)
    # 4. dump result as json
    json.dump(learning, open('corpus.json', 'w'))
    json.dump(testing, open('corpus_testing.json', 'w'))
    json.dump(result_data, open('result.json', 'w'))
    print '>> calculation finish, data dumped in result.json\n'

elif len(sys.argv) > 3:
    try:
        result_data_dir = sys.argv[2]
        corpus_dir = sys.argv[3]
        corpus_testing_dir = sys.argv[4]
        if not os.path.isfile(result_data_dir) and not os.path.isfile(corpus_dir):
            raise Exception('file not found')

        temp = open(result_data_dir)
        result_data = json.load(temp)  # bag_of_words, paired_bag_of_words, unigram, bigram

        temp = open(corpus_dir)
        learning = json.load(temp)

        temp = open(corpus_testing_dir)
        testing = json.load(temp)
    except Exception as e:
        print 'file not found'
else:
    print 'argument not enough'


# bag_of_words, paired_bag_of_words, unigram, bigram = result_data
# print bag_of_words
# print unigram
# print paired_bag_of_words
# print bigram
# analyzer.print_unigram_analysis(testing[1], result_data)
# analyzer.print_bigram_analysis(testing[1], result_data)

for sentence in learning[:-10]:
    analyzer.print_unigram_analysis(sentence, result_data)
    analyzer.print_bigram_analysis(sentence, result_data)

for sentence in testing:
    analyzer.print_unigram_analysis(sentence, result_data)
    analyzer.print_bigram_analysis(sentence, result_data)

# print 'byk learning', len(learning)
