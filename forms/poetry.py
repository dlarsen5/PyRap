#! /usr/bin/env python
from line import Line
from section import Section


class Haiku(Section):
    '''
    3 Lines with 5/7/5 syllable counts
    '''
    def __init__(self, lines=[], name='', topic=''):

        if not lines:
            self.lines = [Line(), Line(), Line()]
        else:
            if len(lines) != 3:
                raise ValueError("Error: Must be 3 lines")
            self.lines = [Line(x) for x in lines]
        self.name = name
        self.topic = topic
        self.description = "3 lines with 5/7/5 syllable counts\n\
                            often focusing on images from nature,\n\
                            emphasizing simplicity, intensity, and\n\
                            directness of expression\n"


class Limerick(Section):
    '''
    5 Lines with 5/7/5 syllable counts
    '''
    def __init__(self, lines=[], name='', topic=''):

        if not lines:
            self.lines = [Line(), Line(), Line(), Line(), Line()]
        else:
            if len(lines) != 5:
                raise ValueError("Error: Must be 3 lines")
            self.lines = [Line(x) for x in lines]
        self.name = name
        self.topic = topic
        self.description = "5 lines with 5/7/5 syllable counts\n\
                            Rhythm pattern is (weak: dashes, strong: backslash):\n\
                            1) -/--/--/\n\
                            2) -/--/--/\n\
                            3) -/--/\n\
                            4) -/--/\n\
                            5) -/--/--/\n\
                            --------------------------------\n\
                            Typically:\n\
                            - the first and second lines rhyme\n\
                            - the third and fourth lines rhyme,\n\
                            - the fifth either repeats the first\n\
                              line or rhymes with it"
