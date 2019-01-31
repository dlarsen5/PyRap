import datetime
import os
from pprint import pprint as pp
import sys
import time

from generate import Generate


if __name__ == '__main__':
    '''
    y/n on word pairs consisting of
    random([adj, adv, verb]) + TopicWord

    once quit, save lines in 'saved/'
    '''

    while True:

        pairs = Generate().pairs()

        pairs = [x[0] + ' ' + x[1] for x in pairs]
        pairs = list(sorted(pairs))
        pairs.sort(key=len)

        save_lines = []

        for p in pairs:

            os.system("clear")
            print(p, '\n', 'y/n?', '\n')

            inp = input()

            if inp == 'j':
                save_lines.append(p)
                print('cool my dude')
                time.sleep(0.05)

            elif inp == 'q':
                break

            else:
                continue

        save_file = 'saved_lines_%s.txt' % datetime.datetime.now().strftime('%d_%m_%Y')

        with open(save_file, 'w') as f:
            for i in save_lines:
                f.write(i + '\n')

        print('\n', "saved file %s" % save_file)
