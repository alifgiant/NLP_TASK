import sys
import os
import iextraction

default_text_address = 'Task2/Chelsea_vs_Burnley.txt'
# default_text_address = 'Task2/Whatford_vs_Arsenal.txt'


def summerize(counter, lines):
    string = 'Today game was very interesting, the game that brought 2 sides {} and {}.\n'
    # print counter
    goals = 0
    chance = 0
    for line, count in zip(lines, xrange(len(lines))):
        if line[1] == 'goal':
            goals += 1
            chance += 1
            if goals == 1:
                string += 'The first goal goes to {} by {}\n'
                # if very soon do
            elif goals == counter['goal']:
                string += 'The last goal goes to {} by {} at {}\n'
            else:
                string += 'next goal goes to {} by {}\n'
                # if tied bla bla
        elif line[1] == 'miss':
            chance += 1
            if chance == 1:
                string += 'The first chance goes to {}, {} but failed to hit the net\n'
                # if very soon do
            elif chance == counter['miss']:
                string += 'The last chance of the game goes to {} with no result\n'
            else:
                string += 'A chance come to {}, {} but failed to hit the net at {}\n'
                # if tied bla bla
    return string


if __name__ == "__main__":

    if len(sys.argv) > 1:
        process_text_address = sys.argv[1]
    else:
        process_text_address = default_text_address

    print 'File address:', process_text_address, '\n'

    if not os.path.isfile(process_text_address):
        print 'process file not found'
    else:
        data = open(process_text_address)
        # do extraction
        event_counter, lines = iextraction.extract_info(data)

        # print event_counter

        # do play
        print summerize(event_counter, lines)


