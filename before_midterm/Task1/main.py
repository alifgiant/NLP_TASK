import re
import file_reader
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

regex_char = '[^a-zA-Z\s]|^\w'


def get_text_counter(paragraphs):

    words = []
    for paragraph in paragraphs:
        lowered_text = paragraph.lower()
        regex = re.compile(regex_char)
        lowered_text = regex.sub('', lowered_text)
        # lowered_text = re.sub(regex_char, ' ', lowered_text)
        splits = re.split(' ', lowered_text)
        words += [item for item in splits]
    word_counter = Counter(words)
    if '' in word_counter:
        word_counter.pop('')

    # print word_counter

    return word_counter

if __name__ == "__main__":
    # training
    train_dir = "dataset/extracted_text.txt"
    # train_dir = "dataset/extracted_text_sampled.txt"
    lines = file_reader.get_target(train_dir)
    res = get_text_counter(lines)

    most10 = res.most_common(10)
    least10 = res.most_common()[-10:]
    # print res.most_common()
    # print most10
    # print least10

    sorted_freq = sorted(res.values(), reverse=True)
    sorted_freq_log = sorted(np.log10(res.values()), reverse=True)

    fig, (real_count_plot, log_count_plot) = plt.subplots(2, 1, sharex=True)
    real_count_plot.plot(sorted_freq)
    log_count_plot.plot(sorted_freq_log, color='r')
    fig.text(0.01, 0.01, 'Most 10: '+str(most10)+'\nLeast 10: '+str(least10), fontsize=13)
    fig.suptitle('Plot Result', fontsize=14, fontweight='bold')
    # print fig.texts[1]
    # fig.('bold figure suptitle', fontsize=14, fontweight='bold')
    plt.show()

