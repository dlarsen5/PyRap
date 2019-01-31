#! /usr/bin/env python
from section import Section


class Song:

    def __init__(self, title='', artist='', theme=''):

        self.sections = {'Chorus': [],
                         'Verse': [],
                         'Hook': [],
                         'Bridge': [],
                         'Intro': [],
                         'Outro': []}
        self.title = title
        self.artist = artist
        self.theme = theme
        # list of tuples (section_name, index)
        self.arrangement = []

    def work_on_section(self, section):

        sec = self.sections[section]

        if len(sec) > 1:
            choice = input('%s sections, which one?' % len(sec))

        return sec

    def song(self):

        song = ''

        if self.arrangement:
            for arrange, index in self.arrangement:
                s = self.sections[arrange][index]
                song.append(str(s) + '\n')

        return song

    def section_count(self):

        count = 0

        for k, v in self.sections:
            count += len(v)

        return v
