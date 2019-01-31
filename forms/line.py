#! /usr/bin/env python
from nltk import *


class Line:
    '''
    Class for managing a single line(list) of words
    '''
    def __init__(self, line=[]):

        if isinstance(line, str):
            self.words = line.split()
        else:
            self.words = line
        self.line = ' '.join(self.words)[1:]
        self.clean_line = self.clean_line()
        self.word_count = len(self.words)
        self.char_count = len(self.line.replace(' ',''))
        self.start_char = self.line[0].lower()
        self.end_word = self.line[-1]
        self.word_pos = self.pos()
        self.pos_stats = ['%s: %s' % (pos, len(words)) for pos, words
                         in self.word_pos.items()]
        self.stats = {'Word Count': self.word_count,
                      'Character Count': self.char_count,
                      'Starting Letter': self.start_char,
                      'Ending Word:': self.end_word,
                      'POS used:': '\n'.join(self.pos_stats)}

    def __str__(self):
        return ' '.join(self.line)[1:]

    def pos(self):
        '''
        Get POS tags for words in line

        Returns
        -------
        word_dict: dict
            - POS dictionary
        '''
        def check_word(word):
            if not wordnet.synsets(word):
                return False
            else:
                return True

        word_dict = {'untagged': []}

        for w in self.words:
            if check_word(w):
                word, pos = nltk.pos_tag([w])[0]
                if pos not in word_dict.keys():
                    word_dict[pos] = [word]
                else:
                    word_dict[pos].append(word)
            else:
                word_dict['untagged'].append(w)

        for k, v in word_dict.items():
            word_dict[k] = sorted(list(set(v)))

        return word_dict

    def clean_line(self):
        '''
        Clean string of bad characters and split to get words
        '''
        bad_characters = ['"', '_', '(', ')', '$', ',', '.', '?', '!', '—','']

        l = self.line
        l_ = []

        for char in l:
            if char in bad_characters:
                continue
            else:
                l_.append(char)

        l = ''.join(l_)

        l = l.split()

        return l
