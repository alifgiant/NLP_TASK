import sys
import os
import iextraction
import summerization

default_text_address = 'Task2/Chelsea_vs_Burnley.txt'
# default_text_address = 'Task2/Whatford_vs_Arsenal.txt'


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

        # # print event_counter
        # print 'res', lines[len(lines)-1][2]

        # do play
        print summerization.summerize(event_counter, lines)
