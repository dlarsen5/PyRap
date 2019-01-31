import os
import sys
import random

from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn

if '../' not in sys.path:
    sys.path.append("../")

from util.wordutil import WordUtil as WU


class Generate:

    def __init__(self):
        self.pos_dict = {}
        self.my_dict = {}
        self.topic_dict = {}
        self.topic_words = []
        self.line_topics = {}
        self.lines = []
        self.conjunctions = ['and', 'but', 'yet', 'or', 'because',
                            'for', 'nor', 'so', 'rather than',
                            'as much as']

    def pairs(self, n_pairs=100, topic=None):
        '''
        Generate pairs of words using the
        formula `pair = topic_word + random[adj, adv, verb]`

        Parameters
        -------
        n_pairs: int
            - Number of pairs to generate
        '''

        if not self.pos_dict:
            self.load_pos_words()

        if not self.my_dict:
            self.load_topics()

        if topic:
            topic_list = self.topic_dict[topic]
        else:
            topic_list = []
            for k, v in self.topic_dict.items():
                topic_list.extend(v)

        pairs = []

        for i in range(0, n_pairs):
            # Same starting letter
            topic = random.choice(topic_list)
            startswith = topic.lower()[0]
            pos = random.choice(['adj', 'adv', 'verb'])
            word_list = self.pos_dict[pos]

            word_list = [x for x in word_list
                        if x.lower().startswith(startswith)]
            if not word_list:
                continue

            modifier = random.choice(word_list)

            pairs.append([modifier, topic])

        return pairs

    def load_topics(self):
        '''
        Get all topic words from "../topics/"

        Returns
        -------
        Set self.topic_dict with self.topic_dict[topic] = topic_words
        '''
        for f in os.listdir('../topics/'):
            topic = f.split('.')[0]

            with open(('../topics/' + f), 'r') as text:
                topic_words = text.readlines()

            topic_words = [x.replace('\n', '') for x in topic_words]

            self.topic_dict[topic] = topic_words

        for k, v in self.topic_dict.items():
            self.topic_words.extend(v)

    def load_pos_words(self):
        '''
        Method to get all tagged POS words from NLTK wordnet

        Returns
        -------
        Set "self.word_dict"
        '''
        pos_map = {
            'noun': wn.NOUN,
            'verb': wn.VERB,
            'adj': wn.ADJ,
            'adv': wn.ADV
        }

        for tag, pos in pos_map.items():
            if tag == 'noun':
                continue

            words = []

            synsets = [x for x in wn.all_synsets(pos)]

            for synset in synsets:
                words.append(synset.lemmas()[0].name())

            words = list(sorted(set(words)))
            if words:
                self.pos_dict[tag] = words

        return

    def get_rhymes(self, word, startswith=''):
        '''
        Wrapper function to WordUtil.get_rhymes

        Parameters
        -------
        word: str
            - Word to get rhymes for

        Returns
        -------
        words: list
            - List of rhyme words
        '''
        wordutil = WU()
        words = wordutil.get_rhymes(word=word,
                                       startswith=startswith)

        return words
