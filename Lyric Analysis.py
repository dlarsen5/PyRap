import pickle
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import os
import pandas as pd

def common_words(lyrics):
    lines = [x for x in lyrics.splitlines() if '[' not in x and x != '']

    w = ' '.join(lines)

    dirty_tokens = word_tokenize(w)

    stopword = set(stopwords.words('english'))

    mystopwords = ['like', 'yeah', 'know', 'they']

    total_stop_words = mystopwords + list(stopword)

    tokens = [word for word in dirty_tokens if word not in total_stop_words]

    small_words = [word.lower() for word in tokens if word.isalpha() and len(word) <= 3]
    words = [word.lower() for word in tokens if word.isalpha() and len(word) > 3]
    total_lyrics = len(words) + len(small_words)
    text = nltk.Text(words)
    fdist = FreqDist(text)

    most_common = fdist.most_common(10)

    values = [len(small_words),total_lyrics,most_common]

    return values

def clean_song_titles(song_dict):
    """

    To clean song titles from features, leaving just the name
    :param song_dict: dictionary of an artist's songs
    :return: cleaned song names and featured artists

    """
    keys = [x.replace(u'\xa0', u' ').replace(u'\u200b', u'') for x in song_dict.keys()]
    cleansed_song_titles = []
    featured_artists = []
    for k in keys:
        if '(' in k:
            if 'ft' in k.lower():
                new_k = k.split('(')[0][:-1]
                featured_artists.append(k.split('(')[1][:-1])
                cleansed_song_titles.append(new_k)
            else:
                cleansed_song_titles.append(k)
        else:
            cleansed_song_titles.append(k)

    return cleansed_song_titles, featured_artists

def main():

    artists_and_lyrics = {}

    for artist in os.listdir('Song Lyrics/'):
        artist_path = 'Song Lyrics/' + artist
        with open(artist_path, 'rb') as f:
            artist_name = artist.replace('_', ' ')
            artists_and_lyrics[artist_name] = pickle.load(f)

    artist_stats = {}

    for artist,song_lyrics in artists_and_lyrics.items():
        all_lyrics = []
        for song,lyrics in song_lyrics.items():
            all_lyrics.append(lyrics)

        lyrics_string = ''.join(all_lyrics)
        values = common_words(lyrics_string)
        artist_stats[artist] = values

    frame = pd.DataFrame(artist_stats).T
    frame.columns = ['Number of Small Words','Number of Total Lyrics','10 Most Used Words W/ Frequencies']
    save_path = 'Statistics.csv'
    if os.path.exists(save_path):
        os.remove(save_path)
    frame.to_csv(save_path)


if __name__ == '__main__':
    main()

