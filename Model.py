import os
import pickle
import random
import re

import pandas as pd
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

artists = ['Kendrick Lamar','Drake','Chance The Rapper','J. Cole','Logic','Future','Chief Keef','Eminem','Kanye West','JAY-Z','Big Sean',
                      'Lil Uzi Vert','Tyler, The Creator','Earl Sweatshirt','2 Chainz','G-Eazy','ScHoolboy Q','Young Thug','Joey Bada$$', 'PnB Rock',
                      'Flatbush Zombies','A$AP Rocky','A$AP Ferg','Dumbfoundead','Tory Lanez','Waka Flocka Flame','Nas','A Tribe Called Quest','Vic Mensa',
                      '$UICIDEBOY$','Denzel Curry','Maxo Kream','Isaiah Rashad','Mike Stud','Mac Miller','Yonas','Childish Gambino','Rich Chigga',
                      'Three 6 Mafia','Azizi Gibson','RiFF RAFF','Lil Dicky','Lil Wayne','Tyga','Gucci Mane','Rick Ross','Asher Roth','Travis Scott','Migos','Rihanna',
                      'Bryson Tiller','21 Savage','Rae Sremmurd','French Montana','Miley Cyrus','XXXTENTACION','Lil Pump','Ski Mask the Slump God','Xavier Wulf',
                      'SmokePurpp','A Boogie Wit Da Hoodie','Playboi Carti','Ugly God','Wiz Khalifa','Justin Bieber','Beyoncé','Nicki Minaj','Meek Mill']

def Clean_Title(song_title):
    new_title = re.sub(r'[^\x00-\x7F]+', ' ', song_title)
    if new_title[-1] == ')':
        ind = new_title.index('(')
        new_title = new_title[:ind]

    return new_title

def Clean_Lyrics(song_lyrics):

    sentence_list = []
    bad_characters = ['_','(',')','$','—','\\']
    bad_words = ['it', 'the', 'you', 'they', 'she', 'he', 'this', 'my', 'to', 'me', 'in', 'like', 'yeah', "you're",
                 "that's", "really", "couldn't",
                 'youre','get','want','come','uh','put','got','one','im',
                 'ran','em','right','gon','need','take','dont','every',
                 'turn','back','lets','better','look','see','til',
                 'aint','tryna','oh','still','yo',"don't","i'm",'gotta',
                 'know','go','yuh']

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

            w = ''.join(new_word)
            words.append(w)
            new_word = []

        if words != []:
            new_line = ' '.join(words)
            sentence_list.append(new_line)

    new_sentence_list = []

    for sent in sentence_list:
        if sent[-1] == '?' or sent[-1] == '!':
            new_sentence_list.append(sent)
            continue
        else:
            sent = sent + '.'
            new_sentence_list.append(sent)

    song_corpus = ' '.join(new_sentence_list)

    return song_corpus

def Lyrics_Corpus():
    song_lyrics_path = 'Song Lyrics/'

    artist_dict = {}

    for root,dirs,files in os.walk(song_lyrics_path):
        for f in files:
            name = root + f
            artist_dict[f.replace('_',' ')] = name

    art_lyrics_full = {}

    for art,path in artist_dict.items():
        title_and_song = {}
        with open(path,'rb') as f:
            lyrics = pickle.load(f)
        for title,song_lyrics in lyrics.items():
            title = Clean_Title(title)
            lyrics = Clean_Lyrics(song_lyrics)
            title_and_song[title] = lyrics

        art_lyrics_full[art] = title_and_song

    return art_lyrics_full

def Artist_DataFrame(list_of_artists):

    def get_artist_frame(artist):

        lyric_sent = Lyrics_Corpus()
        list_of_series = []

        for art, songs in lyric_sent.items():
            art_series = pd.Series(data=songs, name=art)
            list_of_series.append(art_series)

        frame = pd.concat(list_of_series, axis=1, keys=[s.name for s in list_of_series])

        artist_series = frame[artist].dropna().reset_index()

        artist_frame = pd.DataFrame(artist_series)
        artist_frame['y_target'] = artist
        artist_frame.columns = ['Song_Title', 'Lyrics', 'y_target']

        return artist_frame

    list_of_frames = []
    for art in list_of_artists:
        list_of_frames.append(get_artist_frame(art))

    frame = pd.concat(list_of_frames)

    return frame

def Train_And_Test(number_of_artists=None):

    artists_to_test = []

    if number_of_artists == None:
        artists_to_test = artists

    elif number_of_artists > 0:
        for i in range(number_of_artists):
            artists_to_test.append(random.choice(artists))
    else:
        print('Error in amount of artists to test')
        return

    frame = Artist_DataFrame(artists_to_test)

    frame['length'] = frame['Lyrics'].str.count(' ')

    text = list(frame['Lyrics'].values)

    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')

    tf = tf_vectorizer.fit_transform(text)

    train1 ,test1 = train_test_split(frame,test_size=0.2)
    X_train = train1['Lyrics'].values
    X_test = test1['Lyrics'].values
    y_train = train1['y_target'].values
    y_test = test1['y_target'].values

    text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf',svm.LinearSVC())])
    text_clf = text_clf.fit(X_train,y_train)
    y_test_predicted = text_clf.predict(X_test)

    model_pred = y_test_predicted

    wrong_predictions = 0

    for t,m_pred in zip(y_test,model_pred):
        if t != m_pred:
            wrong_predictions += 1

    print("Number of Training Lyrics: %s" % len(X_train))
    print("Number of Test Lyrics: ", len(y_test))
    print("Number of Correct Predictions: ", (len(y_test)-wrong_predictions))
    print("Accuracy: %s" % ((len(y_test)-wrong_predictions)/len(y_test)))

    return