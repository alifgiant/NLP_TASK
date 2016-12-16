import res
import json
import numpy as np
import processing
import itertools


def decode_tags(chains):
    tags = list()
    for chain in chains:
        tags.append(res.PTB_POS_TAGS[chain])
    return tags


def get_possible_tag(pos):
    if pos < 0:
        return ['*']
    return res.PTB_POS_TAGS


def get_predicted_tag(sentence, emission_cpt, transition_unigram, transition_bigram, transition_trigram):
    words = sentence.split(' ')
    words_length = len(words)
    tags_length = len(res.PTB_POS_TAGS)+1  # +1 for *

    dp_prob_matrix = np.ones((words_length, tags_length, tags_length)) * -1
    dp_prob_matrix[-1, 0, 0] = 1
    backpointer_matrix = np.ones((words_length, tags_length, tags_length), dtype=int) * -1

    for k in range(len(words)):
        possible_current = get_possible_tag(k)
        possible_last1 = get_possible_tag(k - 1)

        for u, v in list(itertools.product(range(len(possible_last1)), range(len(possible_current)))):
            current = possible_current[v]
            last1 = possible_last1[u]

            possible_last2 = get_possible_tag(k - 2)
            temp_max = -1

            for w in range(len(possible_last2)):
                word = words[k]
                last2 = possible_last2[w]
                result = dp_prob_matrix[k-1, w, u] \
                         * processing.get_smoothed_transition_probability(current, last1, last2,
                                                                          transition_unigram,
                                                                          transition_bigram,
                                                                          transition_trigram) \
                         * processing.get_emission_probability(word, current, emission_cpt)\
                         # * 1000
                # print (result)
                if result < 0:
                    print 'kwu', k-1, w, u
                    raise Exception('zero / negative found')
                if result > temp_max:
                    temp_max = result
                    backpointer_matrix[k, u, v] = w
            dp_prob_matrix[k, u, v] = temp_max
            # print (temp_max, backpointer_matrix[k, u, v])
            # break
        # break

    # print (dp_prob_matrix)
    # print (np.amax(dp_prob_matrix[len(words)-1]))
    last_pos_dp = dp_prob_matrix[len(words)-1]
    u, v = np.unravel_index(last_pos_dp.argmax(), last_pos_dp.shape)
    predicted_tag = [v, u]
    # print 'arg', u, v
    # print (dp_prob_matrix[len(words)-1, 25, 25])

    current, last1 = v, u
    for i in reversed(range(len(words))[2:]):
        bp = backpointer_matrix[i, last1, current]
        # print (bp)
        current = u
        last1 = bp
        predicted_tag.append(bp)
    return predicted_tag[::-1]


if __name__ == '__main__':
    '''2.5 load processing result'''
    with open(res.DataSet.Training[res.EMISSION_CPT]) as json_data:
        word_emission = json.load(json_data)
    with open(res.DataSet.Training[res.TRANSITION_UNIGRAM]) as json_data:
        transition_unigram = json.load(json_data)
    with open(res.DataSet.Training[res.TRANSITION_BIGRAM]) as json_data:
        transition_bigram = json.load(json_data)
    with open(res.DataSet.Training[res.TRANSITION_TRIGRAM]) as json_data:
        transition_trigram = json.load(json_data)

    sentence = 'the man live in the district'
    # sentence = 'the'
    result = get_predicted_tag(sentence, word_emission, transition_unigram, transition_bigram, transition_trigram)
    tags = decode_tags(result)
    print (tags)

    # dp_matrix = np.ones((5, 3, 3), dtype=int) * -1
    # print (dp_matrix)
    # print (dp_matrix[1])
