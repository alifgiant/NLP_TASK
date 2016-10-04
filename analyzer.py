def print_unigram_analysis(sentence, result_data):
    bag_of_words, paired_bag_of_words, unigram, bigram = result_data
    total_word = sum(bag_of_words.values())
    print 'Unigram model'
    print '========================================================='
    print 'wi             C(wi)       #words       P(wi)'
    print '========================================================='
    words = sentence.split(' ')
    prop = 1
    for word in words[1:]:  # <s> is not needed
        uni = 0.00000000000000000000000000001
        if word in bag_of_words:
            uni = unigram[word]
        print '{0:12s}   {1:9d}   {2:10d}   {3}'.format(word, bag_of_words[word], total_word, uni)
        prop *= unigram[word]
    print '====================================================='
    print 'Prob. unigrams:  ', prop
    # Perplexity is the inverse probability of the test set, normalized by the number of words.
    # In the case of unigrams:
    print 'Perplexity:  ', pow(1./prop, 1./(len(words)-1))  # len(words)-1 because <s> not included


def print_bigram_analysis(sentence, result_data):
    bag_of_words, paired_bag_of_words, unigram, bigram = result_data
    print 'Bigram model'
    print '====================================================================='
    print 'wi             wi+1           Ci,i+1      C(i)        P(wi+1|wi)'
    print '====================================================================='
    words = sentence.split(' ')
    prop = 1
    for i in range(len(words))[:-1]:
        word_i = words[i]
        word_ii = words[i+1]
        ci_ii = 0
        bi = 0.00000000000000000000000000001
        if word_ii in paired_bag_of_words:
            ci_ii = paired_bag_of_words[word_ii][word_i]
        if word_i in paired_bag_of_words[word_ii]:
            bi = bigram[word_ii][word_i]
        print '{0:12s}   {1:12s}   {2:9d}   {3:9d}   {4}'.format(words[i], words[i+1], ci_ii, bag_of_words[word_i], bi)
        prop *= bi
    print '====================================================================='
    print 'Prob. bigrams:  ', prop
    print 'Perplexity:  ', pow(1./prop, 1./(len(words)))