from collections import Counter
import re

def summerize(counter, lines):
    match = re.search('(\w*)\s(\d),\s(\w*)\s(\d)', lines[len(lines)-1][2])

    clubs = [match.group(1), match.group(3)]
    scores = [match.group(2), match.group(4)]
    string = 'Today game was very interesting, the game that brought 2 sides {} and {}.\n'.format(clubs[0],
                                                                                                  clubs[1])
    counter = Counter()
    # print counter
    goals = 0
    chance = 0
    for line, count in zip(lines, xrange(len(lines))):
        match = re.search('\.\s(.*)\s\((.*)\)\s(.*)', line[2])
        if line[1] == 'goal':
            counter[match.group(2)] += 1
            goals += 1
            chance += 1
            if goals == 1:
                string += 'The first goal goes to {} by {}\n'.format(match.group(2), match.group(1))
                # if very soon do
            elif goals == counter['goal']:
                string += 'The last goal goes to {} by {} at {}\n'.format(match.group(2),
                                                                          match.group(1), line[0])
            else:
                string += 'next goal goes to {} by {}\n'.format(match.group(2), match.group(1))
            if counter[clubs[0]] == counter[clubs[1]]:
                string == 'the goal tied the game.\n'
        elif line[1] == 'miss':

            chance += 1
            if chance == 1:
                string += 'The first chance goes to {}, {} but failed to hit the net\n'\
                    .format(match.group(2), match.group(1)+' '+match.group(3))
                # if very soon do
            elif chance == counter['miss']+counter['goal']:

                string += 'The last chance of the game goes to {} with no result\n'\
                    .format(match.group(2))
            else:
                string += 'A chance come to {}, {} but failed to hit the net at {}\n'\
                    .format(match.group(2), match.group(1), line[0])
    string += 'the game end with {} {} and {} {}'.format(clubs[0], scores[0], clubs[1], scores[1])
    return string