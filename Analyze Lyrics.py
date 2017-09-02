import pickle
import os
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import re
import itertools
from gensim import models

def common_words(lyrics):

    lines = [x for x in lyrics.splitlines() if '[' not in x and x != '']

    w = ' '.join(lines)

    dirty_tokens = word_tokenize(w)

    stopword = set(stopwords.words('english'))

    mystopwords = ['like','yeah','know','they']

    total_stop_words = mystopwords + list(stopword)

    tokens = [word for word in dirty_tokens if word not in total_stop_words]


    small_words=[word.lower() for word in tokens if word.isalpha() and len(word) <= 3]
    words=[word.lower() for word in tokens if word.isalpha() and len(word) > 3]
    total_lyrics = len(words) + len(small_words)
    text = nltk.Text(words)
    fdist = FreqDist(text)

    cus_words = ['fuck','shit','damn','hell','bitch','ass','asshole']

    cussin = len([word.lower() for word in tokens if word.lower() in cus_words])
    nigga = len([word.lower() for word in tokens if 'nigga' in word.lower()])

    most_common = fdist.most_common(10)

    values = {'Small Words' : small_words,'Total Words' : total_lyrics,
              '10 Most Common' : most_common, 'Cuse Words' : cussin,
              'Niggas' : nigga}

    return values

def get_verses(all_lyrics,artist):
    #finds total verses, hooks, bridges, choruses written by a specific artist

    one_song_verse_lines = []
    one_song_chorus_lines = []
    one_song_hook_lines = []
    one_song_bridge_lines = []

    total_verse_lines = []
    total_chorus_lines = []
    total_hook_lines = []
    total_bridge_lines = []
    total_lines = []
    Songs = {}

    for art,songs in all_lyrics.items():

        for song_title,song_lyrics in songs.items():
            clean_title = song_title.replace('(','').replace('.','').split()
            if art == artist and 'Ft' not in clean_title:
                lines = song_lyrics.splitlines()
                for l in range(len(lines)):
                    title = [x.lower() for x in lines[l].replace('[', '').replace(']', '').split()]
                    if '[' in lines[l] and 'verse' in title:
                        section_lines = []
                        count = l + 1
                        done = False
                        while count < len(lines) and not done:
                            if '[' not in lines[count]:
                                if lines[count] != '':
                                    section_lines.append(lines[count])
                                count += 1
                            else:
                                done = True
                        total_verse_lines.append(section_lines)
                        one_song_verse_lines.append(section_lines)

                    elif '[' in lines[l] and 'chorus' in title:
                        section_lines = []
                        count = l + 1
                        done = False
                        while count < len(lines) and not done:
                            if '[' not in lines[count]:
                                if lines[count] != '':
                                    section_lines.append(lines[count])
                                count += 1
                            else:
                                done = True
                        total_chorus_lines.append(section_lines)
                        one_song_chorus_lines.append(section_lines)

                    elif '[' in lines[l] and 'hook' in title:
                        section_lines = []
                        count = l + 1
                        done = False
                        while count < len(lines) and not done:
                            if '[' not in lines[count]:
                                if lines[count] != '':
                                    section_lines.append(lines[count])
                                count += 1
                            else:
                                done = True
                        total_hook_lines.append(section_lines)
                        one_song_hook_lines.append(section_lines)

                    elif '[' in lines[l] and 'bridge' in title:
                        section_lines = []
                        count = l + 1
                        done = False
                        while count < len(lines) and not done:
                            if '[' not in lines[count]:
                                if lines[count] != '':
                                    section_lines.append(lines[count])
                                count += 1
                            else:
                                done = True
                        total_bridge_lines.append(section_lines)
                        one_song_bridge_lines.append(section_lines)

            artist_first_name = artist.split()[0].lower()

            if 'Ft' in clean_title:
                lines = song_lyrics.splitlines()
                for l in range(len(lines)):
                    title = [x.lower() for x in lines[l].replace('[','').replace(']','').replace('-','').replace(':','').split()]
                    if '[' in lines[l] and 'verse' in title and artist_first_name in title:
                        section_lines = []
                        count = l + 1
                        done = False
                        while count < len(lines) and not done:
                            if '[' not in lines[count]:
                                if lines[count] != '':
                                    section_lines.append(lines[count])
                                count += 1
                            else:
                                done = True
                        total_verse_lines.append(section_lines)
                        one_song_verse_lines.append(section_lines)

                    elif '[' in lines[l] and 'chorus' in title and artist_first_name in title:
                        section_lines = []
                        count = l + 1
                        done = False
                        while count < len(lines) and not done:
                            if '[' not in lines[count]:
                                if lines[count] != '':
                                    section_lines.append(lines[count])
                                count+=1
                            else:
                                done = True
                        total_chorus_lines.append(section_lines)
                        one_song_chorus_lines.append(section_lines)

                    elif '[' in lines[l] and 'hook' in title and artist_first_name in title:
                        section_lines = []
                        count = l + 1
                        done = False
                        while count < len(lines) and not done:
                            if '[' not in lines[count]:
                                if lines[count] != '':
                                    section_lines.append(lines[count])
                                count+=1
                            else:
                                done = True
                        total_hook_lines.append(section_lines)
                        one_song_hook_lines.append(section_lines)

            if len(one_song_verse_lines) > 0:
                total_lines.append(total_verse_lines)
                one_song_verse_lines = []
            if len(one_song_chorus_lines) > 0:
                total_lines.append(total_chorus_lines)
                one_song_chorus_lines = []
            if len(one_song_hook_lines) > 0:
                total_lines.append(total_hook_lines)
                one_song_hook_lines = []
            if len(one_song_bridge_lines) > 0:
                total_lines.append(total_bridge_lines)
                one_song_bridge_lines = []

            if len(total_lines) > 0:
                Songs[song_title] = list(itertools.chain.from_iterable(total_lines))

            total_lines = []


    Lines = {'Verses':total_verse_lines,'Choruses':total_chorus_lines,'Hooks':total_hook_lines,'Bridges':total_bridge_lines}

    return Lines, Songs

def clean_name(song_title):
    return re.sub(r'[^\x00-\x7F]+', ' ', song_title)

def clean_song_titles(song_dict):
    keys = [x.replace(u'\xa0', u' ').replace(u'\u200b',u'') for x in song_dict.keys()]
    new_keys = []
    featured_artists = []
    for k in keys:
        if '(' in k:
            if 'ft' in k.lower():
                new_k = k.split('(')[0][:-1]
                featured_artists.append(k.split('(')[1][:-1])
                new_keys.append(new_k)
            else:
                new_keys.append(k)
        else:
            new_keys.append(k)

    return new_keys,featured_artists

artists = ['Kendrick Lamar','Drake','Chance The Rapper','J. Cole','Logic','Future','Chief Keef','Eminem','Kanye West','JAY-Z','Big Sean',
                      'Lil Uzi Vert','Tyler, The Creator','Earl Sweatshirt','2 Chainz','G-Eazy','ScHoolboy Q','Young Thug','Joey Bada$$', 'PnB Rock',
                      'Flatbush Zombies','A$AP Rocky','A$AP Ferg','Dumbfoundead','Tory Lanez','Waka Flocka Flame','Nas','A Tribe Called Quest','Vic Mensa',
                      '$UICIDEBOY$','Denzel Curry','Maxo Kream','Isaiah Rashad','Mike Stud','Mac Miller','Yonas','Childish Gambino','Rich Chigga',
                      'Three 6 Mafia','Azizi Gibson','RiFF RAFF','Lil Dicky','Lil Wayne','Tyga','Gucci Mane','Rick Ross','Asher Roth','Travis Scott','Migos','Rihanna',
                      'Bryson Tiller','21 Savage','Rae Sremmurd','French Montana','Miley Cyrus','XXXTENTACION','Lil Pump','Ski Mask the Slump God','Xavier Wulf',
                      'SmokePurpp','A Boogie Wit Da Hoodie','Playboi Carti','Ugly God','Wiz Khalifa','Justin Bieber','Beyoncé','Nicki Minaj','Meek Mill']

def make_lists(Lines,lyric_type):

    sentence_list = []
    bad_characters = ['"',"'",'_','(',')','$',',','.','?','!','—']

    for lst in Lines[lyric_type]:
        for ele in lst:
            new_word = []
            separate = ele.split()
            words = []
            for word in separate:
                for character in word:
                    character = character.lower()
                    if character not in bad_characters:
                        new_word.append(character)

                words.append(''.join(new_word))
                new_word = []

            sentence_list.append(words)

    return sentence_list

def make_one_list(song_lyrics):

    sentence_list = []
    bad_characters = ['"',"'",'_','(',')','$',',','.','?','!','—']

    lines = song_lyrics.splitlines()

    for line in lines:
        if line == '\n':
            continue
        if '[' in line:
            continue
        new_word = []
        separate = line.split()
        words = []
        for word in separate:
            for character in word:
                character = character.lower()
                if character not in bad_characters:
                    new_word.append(character)

            words.append(''.join(new_word))
            new_word = []
        if words != []:
            sentence_list.append(words)

    return sentence_list

def Get_Artist_Lyrics(artist):
    song_lyrics_path = 'Song Lyrics/'

    artist_dict = {}


    for root,dirs,files in os.walk(song_lyrics_path):
        for f in files:
            name = root + f
            artist_dict[f.replace('_',' ')] = name

    all_lyrics = {}
    for art,path in artist_dict.items():
        with open(path,'rb') as f:
            all_lyrics[art] = pickle.load(f)

    Lines,Songs = get_verses(all_lyrics,artist)

    return Lines, Songs, all_lyrics

def Get_Lyrics():
    song_lyrics_path = 'Song Lyrics/'

    artist_dict = {}


    for root,dirs,files in os.walk(song_lyrics_path):
        for f in files:
            name = root + f
            artist_dict[f.replace('_',' ')] = name

    all_lyrics = []

    for art,path in artist_dict.items():
        with open(path,'rb') as f:
            lyrics = pickle.load(f)
        for title,song_lyrics in lyrics.items():
            lyrics = make_one_list(song_lyrics)
            all_lyrics+=lyrics



    return all_lyrics

def Get_All_Lyrics(all_lyrics):

    sentence_list = []
    bad_characters = ['"',"'",'_','(',')','$',',','.','?','!','—']

    for artist,songs in all_lyrics.items():
        for title,song in songs.items():
            new_word = []
            separate = song.split()
            words = []
            for word in separate:
                for character in word:
                    character = character.lower()
                    if character not in bad_characters:
                        new_word.append(character)

                words.append(''.join(new_word))
                new_word = []

            sentence_list.append(words)

    return sentence_list

#one artist's values
Lines, Songs, All_lyrics = Get_Artist_Lyrics('Drake')

def main():
    full_sent = Get_Lyrics()

    sent = make_lists(Lines,'Verses')

    model = models.Word2Vec(full_sent,min_count=1)

    return model, sent

model = models.Word2Vec.load('word2vecmodel')