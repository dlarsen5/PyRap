import datetime
import os
from pprint import pprint as pp
import sys
import time
import random

from generate import Generate


if __name__ == '__main__':
    '''
    y/n on lines

    once quit, save lines in 'savedlines/'
    '''
    conjunctions = ['and', 'but', 'yet', 'or', 'because',
                        'for', 'nor', 'so', 'rather than',
                        'as much as']

    compares = ['is better than',
              'is worse than',
              'could never defeat a',
              'would win in a fight with a',
              'could never fuck a',
              'always made me feel like a',
              'could never be as good as a']

    createstuff = Generate()
    createstuff.load_lines()

    lines = createstuff.lines

    save_lines = []

    for l in lines:

        os.system("clear")

        rand_l = random.choice(lines)

        out_l = l + ' ' + random.choice(compares) + ' ' + rand_l

        print(out_l, '\n', 'y/n?', '\n')

        inp = input()

        if inp == 'j':
            save_lines.append(p)
            print('cool my dude')
            time.sleep(0.05)

        elif inp == 'q':
            break

        else:
            continue

    save_file = 'savedlines/%s.txt' % datetime.datetime.now().strftime('%d_%m_%Y')

    with open(save_file, 'w') as f:
        for i in save_lines:
            f.write(i + '\n')

    print('\n', "saved file %s" % save_file)
