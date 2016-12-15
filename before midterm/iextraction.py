import re
from collections import Counter


def extract_info(data):
    pattern = '([\d]+\'[+\d\']*)*([a-zA-Z\s][^A-Z]+)(.*)[\r\n]*'
    lines = re.findall(pattern, data.read())[::-1][1:]
    # print "data1:", lines[0], lines[0][0]
    event_counter = Counter([line[1] for line in lines])

    return event_counter, lines

    # for string, count in zip(strings, range(len(strings))):
    #     print 'data', count, ':', strings[count]
