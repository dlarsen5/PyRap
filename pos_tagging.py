from Analyze_Lyrics import Get_Artist_Lyrics
from my_notes_data_handle import get_multiple

from nltk import pos_tag, word_tokenize

import random

def get_my_words():

    train_text = get_multiple(how_many_docs=5)

    my_words = []

    for w in train_text:
        pos_tagged = pos_tag([w])
        my_words.append(pos_tagged[0])

    pos = set([tagged_word[1] for tagged_word in my_words])
    init_pos_array = [[] for _ in range(0,len(pos))]

    my_word_dict = dict(zip(pos,init_pos_array))

    for tagged_word in my_words:

        p = tagged_word[1]
        w = tagged_word[0]
        if w not in my_word_dict[p]:
            my_word_dict[p].append(w)

    return my_word_dict

Lines, Songs, All_lyrics = Get_Artist_Lyrics('Earl Sweatshirt')

verses = Lines['Verses']
bridges = Lines['Bridges']
choruses = Lines['Choruses']
hooks = Lines['Hooks']

tagged_verses = []

for each_block in verses:
    lines = []
    for line in each_block:
        tokenized_text = word_tokenize(line)
        pos_tagged_line = pos_tag(tokenized_text)
        lines.append(pos_tagged_line)
    tagged_verses.append(lines)

my_word_dict = get_my_words()

for verse in tagged_verses[3:5]:
    for line in verse:
        no_print = ['POS','IN','DT','IN','CC','MD',","]
        # print([word[0] + ' ' + word[1] for word in line])
        tags = [word[1] for word in line if word[1] != ',']
        my_words = []
        my_w = ''
        for t in tags:
            try:
                my_words.append(my_word_dict[t][random.randint(0,len(my_word_dict[t])-1)])
            except:
                my_words.append('')
                continue
        print('<----------------------------------------------------------------->')
        print([word[0] for word in line if word[1] != ','])
        print(tags)
        print(my_words)
        print('\n')

print('hi')