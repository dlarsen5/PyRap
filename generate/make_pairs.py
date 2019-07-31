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

    Parameters
    -------
    n_pairs: int
        - Number of pairs to generate
        - Ex: python make_pairs.py 420
    '''
    n_pairs = 100

    if len(sys.argv) > 1:
        n_pairs = int(sys.argv[1])

    pairs = Generate().pairs(n_pairs=n_pairs)

    pairs = [x[0] + ' ' + x[1] for x in pairs]
    pairs = list(sorted(pairs))
    pairs.sort(key=len)

    save_lines = []

    for p in pairs:
        os.system('clear')
        print(p, '\n', 'y/n?', '\n')
        inp = input()
        if inp == 'j':
            save_lines.append(p)
            os.system('clear')
        elif inp == 'q':
            break
        else:
            continue

    save_file = 'saved/%s.txt' % datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

    with open(save_file, 'w') as f:
        for i in save_lines:
            f.write(i + '\n')

    os.system('clear')
    print('\n', "saved file %s" % save_file.split('/')[-1], '\n')
