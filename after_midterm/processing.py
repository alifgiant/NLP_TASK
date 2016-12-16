from collections import Counter
import res
import json


def do_processing(dataset_type, sentences, tag_chains, tag_token_counter):
    # 1. build word-tags count, what possible tag for a word
    word_to_tag_count = dict()
    for sentence, tag_chain in zip(sentences, tag_chains):
        words = sentence.split(' ')
        tags = tag_chain.split(' ')
        for word, tag in zip(words, tags):
            if word not in word_to_tag_count:
                word_to_tag_count[word] = Counter()
                for tag_token in tag_token_counter:  # smooth value
                    word_to_tag_count[word][tag_token] += 1
            word_to_tag_count[word][tag] += 1
            # break

    # 2. build emission CPT from word-tags count
    word_emission = dict()
    for word in word_to_tag_count:
        total_appearance = sum(word_to_tag_count[word].values())
        word_emission[word] = dict()
        for tag in word_to_tag_count[word]:
            word_emission[word][tag] = word_to_tag_count[word][tag] / float(total_appearance)

    # 3. tags unigram, bigram, trigram count
    tags_unigram_count = Counter()
    tags_bigram_count = dict()
    tags_trigram_count = dict()
    for current_tag in res.PTB_POS_TAGS:  # smoothing value
        tags_unigram_count[current_tag] += 1  # count unigram
        tags_bigram_count[current_tag] = Counter()
        tags_trigram_count[current_tag] = dict()
        added_tags = res.PTB_POS_TAGS + ['*']
        for last_1_tag in added_tags:
            tags_bigram_count[current_tag][last_1_tag] += 1  # count bigram
            tags_trigram_count[current_tag][last_1_tag] = Counter()
            for last_2_tag in added_tags:
                tags_trigram_count[current_tag][last_1_tag][last_2_tag] += 1  # count trigram

    for tag_chain in tag_chains:  # real value
        tags = tag_chain.split(' ')
        for i in range(len(tags)):
            current_tag = tags[i]
            if i - 1 < 0:  # i-1 < 0, so i-2 < 0
                last_1_tag = '*'
                last_2_tag = '*'
            else:
                last_1_tag = tags[i - 1]
                if i - 2 < 0:
                    last_2_tag = '*'
                else:
                    last_2_tag = tags[i - 2]
            tags_unigram_count[current_tag] += 1  # count unigram
            tags_bigram_count[current_tag][last_1_tag] += 1  # count bigram
            tags_trigram_count[current_tag][last_1_tag][last_2_tag] += 1  # count trigram
            # break

    # 4. build transition unigram, bigram, trigram CPT
    transition_unigram = dict()
    transition_bigram = dict()
    transition_trigram = dict()

    total_unigram = sum(tags_unigram_count.values())
    for current_tag in tags_unigram_count:
        transition_unigram[current_tag] = tags_unigram_count[current_tag] / float(total_unigram)

    for current_tag in tags_bigram_count:
        transition_bigram[current_tag] = dict()
        total_bigram = sum(tags_bigram_count[current_tag].values())
        for last_1_tag in tags_bigram_count[current_tag]:
            transition_bigram[current_tag][last_1_tag] = tags_bigram_count[current_tag][last_1_tag] / float(
                total_bigram)

    for current_tag in tags_trigram_count:
        transition_trigram[current_tag] = dict()
        for last_1_tag in tags_trigram_count[current_tag]:
            transition_trigram[current_tag][last_1_tag] = dict()
            total_trigram = sum(tags_trigram_count[current_tag][last_1_tag].values())
            for last_2_tag in tags_trigram_count[current_tag][last_1_tag]:
                transition_trigram[current_tag][last_1_tag][last_2_tag] \
                    = tags_trigram_count[current_tag][last_1_tag][last_2_tag] / float(total_trigram)

    # 5. save building result
    res.save_data(dataset_type[res.EMISSION_CPT], [json.dumps(word_emission)], end_flag=False)
    res.save_data(dataset_type[res.TRANSITION_UNIGRAM], [json.dumps(transition_unigram)], end_flag=False)
    res.save_data(dataset_type[res.TRANSITION_BIGRAM], [json.dumps(transition_bigram)], end_flag=False)
    res.save_data(dataset_type[res.TRANSITION_TRIGRAM], [json.dumps(transition_trigram)], end_flag=False)
