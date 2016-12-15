import re
import res

PTB_POS_TAGS = [
    '$',
    '``',
    '\'\'',
    '(',
    ')',
    ',',
    '--',
    '.',
    ':',
    'CC',
    'CD',
    'DT',
    'EX',
    'FW',
    'IN',
    'JJ',
    'JJR',
    'JJS',
    'LS',
    'MD',
    'NN',
    'NNP',
    'NNPS',
    'NNS',
    'PDT',
    'POS',
    'PRP',
    'PRP$',
    'RB',
    'RBR',
    'RBS',
    'RP',
    'SYM',
    'TO',
    'UH',
    'VB',
    'VBD',
    'VBG',
    'VBN',
    'VBP',
    'VBZ',
    'WDT',
    'WP',
    'WP$',
    'WRB',
    'USR',
    'HT',
    'RT',
    'URL',
]  # http://www.comp.leeds.ac.uk/ccalas/tagsets/upenn.html


# Bikel et. al 1999, named entity recognition, +OtherCap (LoL, aWWk)
class LowFrequency(object):
    TwoDigitNum = '[twoDigitNum]'
    FourDigitNum = '[fourDigitNum]'
    ContainsDigitAndAlpha = '[containsDigitAndAlpha]'
    ContainsDigitAndDash = '[containsDigitAndDash]'
    ContainsDigitAndSlash = '[containsDigitAndSlash]'
    ContainsDigitAndComma = '[containsDigitAndComma]'
    ContainsDigitAndPeriod = '[containsDigitAndPeriod]'
    OtherNum = '[otherNum]'
    AllCaps = '[allCaps]'
    CapPeriod = '[capPeriod]'
    FirstWord = '[firstWord]'
    InitCap = '[initCap]'
    Lowercase = '[lowercase]'
    Other = '[other]'
    OtherCap = '[otherCap]'


class TwitterWord(object):
    URL = '[http]'
    HT = '[hashtag]'
    USER = '[user]'
    SYMBOL = '[symbol]'


def normalize_twitter_word(word):
    if not res.is_ascii(word):
        return TwitterWord.SYMBOL
    elif re.match('Http://|\*\*Http://|http://|\**http://', word) is not None:
        return TwitterWord.URL
    elif re.match('#|\*\*#', word) is not None:
        return TwitterWord.HT
    elif re.match('@|\*\*@', word) is not None:
        return TwitterWord.USER
    else:
        return word


def normalize_low_freq(word):
    result = re.search('[0-9]+', word)
    if result is not None:
        if re.search('[a-zA-Z]+', word) is not None:
            return LowFrequency.ContainsDigitAndAlpha
        elif re.search('[-]+', word) is not None:
            return LowFrequency.ContainsDigitAndDash
        elif re.search('[/]+', word) is not None:
            return LowFrequency.ContainsDigitAndSlash
        elif re.search('[,]+', word) is not None:
            return LowFrequency.ContainsDigitAndComma
        elif re.search('[.]+', word) is not None:
            return LowFrequency.ContainsDigitAndPeriod
        elif len(word) == 2:
            return LowFrequency.TwoDigitNum
        elif len(word) == 4:
            return LowFrequency.FourDigitNum
        else:
            return LowFrequency.OtherNum
    result = re.search('[A-Z]+', word)
    if result is not None:
        if re.search('[.]+', word) is not None:
            return LowFrequency.CapPeriod
        elif result.group(0) == word:
            return LowFrequency.AllCaps
        elif word[:2] == '**':
            return LowFrequency.FirstWord
        elif result.group(0) == word[0]:
            return LowFrequency.InitCap
        else:
            return LowFrequency.OtherCap
    elif re.search('[a-z]+', word) is not None:
        return LowFrequency.Lowercase
    else:
        return LowFrequency.Other


if __name__ == '__main__':
    # print (normalize_low_freq('90/'))
    word = 'Http://www.google.com'
    # result = re.search('[A-Z]+', word)
    # if result.group(0) == word:
    res = re.search('http://|Http://', word)
    print (res is None)
    print (res.group(0))

