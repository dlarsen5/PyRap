import sys
import os
import random
from pprint import pprint as pp

if '../' not in sys.path:
    sys.path.append("../")

from genius.lyrics import ConvertLyrics as cl
from util.wordutil import WordUtil as wu
from generate import Generate as gen


class Replace:

    def __init__(self, artist=''):
        self.r = wu()
        self.c = cl()
        self.artists = self.r.artists
        if not artist:
            artist = self.artists[random.randrange(0, len(self.artists))]
        self.artist = artist

    def replace_rap(self):
        '''
        Get topic and words and try to replace all tagged POS in songs
        '''
        self.r.load_rap_pos()

        replace_dict = self.r.rap_pos
        rep = self.c.replace_lyrics(self.artist, replace_dict)

        for title, sections in self.c.replaced_songs.items():
            for sec_name, lines in sections.items():
                os.system('clear')
                print('\n')
                print("---------------------------%s-%s-%s--------------------------" % (self.artist, title, sec_name))
                print('\n')
                for sec in lines:
                    pp(' '.join([x for x in sec if x != '']))
                _inp = input()
                if _inp == 'q':
                    return

    def replace_rapnouns(self):
        '''
        Get topic words and replace nouns in songs with topics
        '''
        topic_words = gen()
        topic_words.load_topics()
        words = topic_words.topic_words

        mydict = {'NN': words}

        rep = self.c.replace_lyrics(self.artist, mydict)

        for title, sections in self.c.replaced_songs.items():
            for sec_name, lines in sections.items():
                os.system('clear')
                print('\n')
                print("---------------------------%s-%s-%s--------------------------" % (self.artist, title, sec_name))
                print('\n')
                for sec in lines:
                    print('\n'.join([x for x in sec if x != '']))
                _inp = input()
                if _inp == 'q':
                    return


if __name__ == '__main__':

    rep = Replace()
    rep.replace_rapnouns()
