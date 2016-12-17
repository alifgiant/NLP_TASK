from collections import Counter
import time
import res
import json
import viterbi
import numpy as np
# ------------------------------------------------------------------------ #

start = time.time()
'''
' 1. Pre processing
' uncomment to re-do pre processing
'''
# region pre processing
# import preprocessing
# data_set = res.load_data(res.DataSet.Training, res.RAW)
# # data_set = res.load_data(res.DataSet.Testing, res.RAW)
# preprocessing.do_pre_processing(data_set, res.DataSet.Training)
# # preprocessing.do_pre_processing(data_set, res.DataSet.Testing)
# # endregion

stop_pre_processing = time.time()
# print ('execution pre processing:', stop_pre_processing - start)

'''1.5 load pre processing result'''
sentences = res.load_data(res.DataSet.Training, res.PREPROCESSED_SENTENCE)
tag_chains = res.load_data(res.DataSet.Training, res.PREPROCESSED_TAGS)
temp_tag_token_counter = res.load_data_with_split(res.DataSet.Training, res.TAG_TOKENS, split_char=' ')
# sentences = res.load_data(res.DataSet.Testing, res.PREPROCESSED_SENTENCE)
# tag_chain = res.load_data(res.DataSet.Testing, res.PREPROCESSED_TAGS)
# temp_tag_token_counter = res.load_data_with_split(res.DataSet.Testing, res.TAG_TOKENS, split_char=' ')

'''
' 2. Processing
' uncomment to re-do processing
'''
# tag_token_counter = Counter()
# for row in temp_tag_token_counter:  # return saved data to counter
#     tag_token_counter[row[0]] = int(row[1])
# # region processing
# import processing
# processing.do_processing(res.DataSet.Testing, sentences, tag_chains, tag_token_counter)
# # processing.do_processing(res.DataSet.Training, sentences, tag_chains, tag_token_counter)
stop_processing = time.time()
print ('execution processing:', stop_processing-stop_pre_processing)

'''2.5 load processing result'''
with open(res.DataSet.Training[res.EMISSION_CPT]) as json_data:
    word_emission = json.load(json_data)
with open(res.DataSet.Training[res.TRANSITION_UNIGRAM]) as json_data:
    transition_unigram = json.load(json_data)
with open(res.DataSet.Training[res.TRANSITION_BIGRAM]) as json_data:
    transition_bigram = json.load(json_data)
with open(res.DataSet.Training[res.TRANSITION_TRIGRAM]) as json_data:
    transition_trigram = json.load(json_data)

'''
' 3. Testing
' - using training dataset
' - using testing dataset
'''
# region testing
i = 0
tag_match, total_tag = 0, 0
tag_chain_match, total_tag_chain = 0, len(tag_chains)
for sentence, tag_chain in zip(sentences, tag_chains):    
    predict_tags = viterbi.get_predicted_tag(sentence, word_emission, transition_unigram, transition_bigram, transition_trigram)
    predict_tags = viterbi.decode_tags(predict_tags)
    target_tags = tag_chain.split(' ')
    miss = False
    for predict, target in zip(predict_tags, target_tags):
        total_tag += 1
        if predict != target:
            miss = True
            continue
        tag_match += 1
    if not miss:
        tag_chain_match += 1
    print ('-----------data---------', total_tag, i+1)
    print ('tag match', tag_match)
    print ('chain match', tag_chain_match)
    i += 1
    # print (target_tags)
    # print (predict_tags)
    # if i == 15:
    #     break

print ('accuracy tag:', tag_match/float(total_tag))
print ('accuracy tweet:', tag_chain_match/float(total_tag_chain))

# endregion
stop_testing = time.time()
print ('execution testing:', stop_testing-stop_processing)
# endregion
