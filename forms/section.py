#! /usr/bin/env python
from line import Line


class Section:

    def __init__(self, lines=[], name='', topic=''):
        '''
        Sections are 3D matrix
            - Ex: Chorus: [chorus1, chorus2]
            - chorus1: [['words', words'],
                        ['words', 'words']]
            - chorus2: [[], [], []]
            - chorus2: [line, line, line]
        '''
        self.lines = [Line(x) for x in lines]
        self.name = name
        self.topic = topic
        self.line_count = len(lines)
        self.line_word_count = [x.word_count for x in self.lines]

    def __str__(self):
        '''
        Custom string representation
        '''
        sec_list = []

        if not self.lines:
            return ''

        for l in self.lines:
            join_line = ' '.join(l)[1:]
            sec_list.append(join_line)
        s = '\n'.join(sec_list)[1:]

        return s

    def save(self):
        '''
        Save section to text file using section name as file name
        '''
        save_p = self.name
        with open(save_p, 'w') as f:
            for l in self.lines:
                f.write(str(l) + '\n')

    def load(self, path):
        '''
        Load section from path

        Parameters
        -------
        path: str
        '''
        with open(path, 'r') as f:
            data = f.read()

        lines = data.split()

        self.lines = [Line(x) for x in lines]

        return
