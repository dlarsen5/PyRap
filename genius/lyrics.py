from nltk.corpus import wordnet
import nltk

import os
import re
import pickle
import random


class Lyrics:

    def __init__(self):
        self.lyrics_path = '../lyrics/'
        self.artists = ['Kendrick Lamar', 'Drake', 'Chance The Rapper', 'J. Cole',
                        'Logic', 'Future', 'Chief Keef', 'Eminem', 'Kanye West',
                        'JAY-Z', 'Big Sean', 'Lil Uzi Vert', 'Tyler, The Creator',
                        'Earl Sweatshirt', '2 Chainz', 'G-Eazy', 'ScHoolboy Q',
                        'Young Thug', 'Joey Bada$$', 'PnB Rock', 'Flatbush Zombies',
                        'A$AP Rocky', 'A$AP Ferg', 'Dumbfoundead', 'Tory Lanez',
                        'Waka Flocka Flame', 'Nas', 'A Tribe Called Quest', 'Vic Mensa',
                        '$UICIDEBOY$', 'Denzel Curry', 'Maxo Kream', 'Isaiah Rashad',
                        'Mike Stud', 'Mac Miller', 'Yonas', 'Childish Gambino', 'Rich Chigga',
                        'Three 6 Mafia', 'Azizi Gibson', 'RiFF RAFF', 'Lil Dicky',
                        'Lil Wayne', 'Tyga', 'Gucci Mane', 'Rick Ross', 'Asher Roth',
                        'Travis Scott', 'Migos', 'Rihanna', 'Bryson Tiller', '21 Savage',
                        'Rae Sremmurd', 'French Montana', 'Miley Cyrus', 'XXXTENTACION',
                        'Lil Pump', 'Ski Mask the Slump God', 'Xavier Wulf', 'SmokePurpp',
                        'A Boogie Wit Da Hoodie', 'Playboi Carti', 'Ugly God', 'Wiz Khalifa',
                        'Justin Bieber', 'Beyoncé', 'Nicki Minaj', 'Meek Mill']

    def clean_title(self, title):
        return re.sub(r'[^\x00-\x7F]+', ' ', title)

    def get_artist_songs(self, artist):
        '''
        Get the organized lyrics for all of an artist's songs

        Parameters
        -------
        artist: str

        Returns
        -------
        songs: dict
            - Dict of organized lyrics by song title
        '''
        lyric_p = [self.lyrics_path + x for x in
                   os.listdir(self.lyrics_path)
                   if x.replace('.pickle', '').replace('_', ' ') == artist][0]

        with open(lyric_p, 'rb') as f:
            song_dict = pickle.load(f)

        songs = {}

        for title, lyrics in song_dict.items():
            organized_lyrics = self.get_lyrics(lyrics)
            title = self.clean_title(title)
            songs[title] = organized_lyrics

        return songs

    def get_lyrics(self, song_lyrics):
        '''
        Convert string of lyrics into Verses, Choruses, Hooks, and Bridges

        Parameters
        -------
        song_lyrics: str
            - Giant string of lyrics for one song

        Returns
        -------
        organized_lyrics: dict
            - Dict of lyrics by Verse, Chorus, Hook, and Bridge
            - Each section (dict key) can have multiple sections
                - Ex: multiple verses, multiple choruses
        '''
        verse_lines = []
        chorus_lines = []
        hook_lines = []
        bridge_lines = []

        lines = song_lyrics.splitlines()

        for l in range(len(lines)):
            line = lines[l].lower()

            if line == '\n':
                continue

            if '[' in line and 'verse' in line:
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
                verse_lines.append(section_lines)

            elif '[' in line and 'chorus' in line:
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
                chorus_lines.append(section_lines)

            elif '[' in line and 'hook' in line:
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
                hook_lines.append(section_lines)

            elif '[' in lines and 'bridge' in line:
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
                bridge_lines.append(section_lines)

        organized_lyrics = {'Verse': verse_lines,
                            'Chorus': chorus_lines,
                            'Hook': hook_lines,
                            'Bridge': bridge_lines}

        return organized_lyrics


class ConvertLyrics:
    '''
    Class for Handling Lyrics
    '''
    def __init__(self):
        self.lyrics = Lyrics()
        self.organized_songs = None

    def _print(type):
        def _my_decorator(view_func):
            def _decorator(request, *args, **kwargs):
                response = view_func(request, *args, **kwargs)

                return response

            return wraps(view_func)(_decorator)

    def convert_artist(self, artist, save=False):
        songs = self.lyrics.get_artist_songs(artist)
        organized_songs = {}

        for title, unclean_song_sections in songs.items():
            song_sections = {}
            for section, lines in unclean_song_sections.items():
                if lines:
                    song_sections[section] = lines

            organized_songs[title] = song_sections

        if save:
            save_p = 'organized_lyrics/%s_organized.pickle' % artist
            with open(save_p, 'wb') as f:
                pickle.dump(organized_songs, f)

        self.organized_songs = organized_songs

        return organized_songs

    def pos(self, artist, save=False):
        '''
        Get words by pos used in songs

        Parameters
        -------
        artist: str
            - Artist name to get lyrics for
        '''
        songs = self.lyrics.get_artist_songs(artist)

        pos_dict = {}

        for title, unclean_song_sections in songs.items():
            for section, lines in unclean_song_sections.items():
                for sub_section in lines:
                    for w in sub_section:
                        if self.check_pos(w):
                            pos = self.get_pos(w)
                            if pos not in list(pos_dict.keys()):
                                pos_dict[pos] = [w]
                            else:
                                pos_dict[pos].append(w)

        if save:
            save_p = 'rapwordlists/%s.pickle' % artist
            with open(save_p, 'wb') as f:
                pickle.dump(pos_dict, f)

        self.rap_pos = pos_dict

        return

    def check_pos(self, w):
        '''
        Check if word is in POS synset

        Parameters
        -------
        w: str
        '''
        if not wordnet.synsets(w):
            return False
        else:
            return True

    def get_pos(self, w):
        '''
        Get POS of a word

        Parameters
        -------
        w: str
        '''
        word, pos = nltk.pos_tag([w])[0]

        return pos
    
    def replace_lyrics(self, artist, mydict, save=False):
        '''
        Replace words by pos used in songs

        Parameters
        -------
        artist: str
            - Artist name to get lyrics for
        '''
        songs = self.lyrics.get_artist_songs(artist)

        replaced_songs = {}

        for title, unclean_song_sections in songs.items():
            new_sections = {}
            for section, sub_section in unclean_song_sections.items():
                for lines in sub_section:
                    new_lines = []
                    for line in lines:
                        new_line = []
                        line = line.split()
                        for w in line:
                            if self.check_pos(w):
                                pos = self.get_pos(w)
                                if pos in mydict.keys(): 
                                    if mydict[pos]:
                                        startswith = w.lower()[0]
                                        words = mydict[pos]
                                        sim_words = [x for x in words if x.startswith(startswith)]
                                        if sim_words:
                                            words = sim_words
                                        rand_ind = random.randrange(0, len(words))
                                        new_word = words[rand_ind].lower()
                                        new_word = '(%s) %s' % (pos,new_word)
                                        new_line.append(new_word)
                                    else:
                                        new_line.append(w)
                                else:
                                    new_line.append(w)
                            else:
                                new_line.append(w)

                        new_line = ' '.join(new_line)

                        if new_line != '':
                            new_lines.append(new_line)

                    if section not in new_sections.keys():
                        new_sections[section] = [new_lines]
                    else:
                        new_sections[section].append(new_lines)

            replaced_songs[title] = new_sections

        if save:
            save_p = 'replaced/%s_replaced.pickle' % artist
            with open(save_p, 'wb') as f:
                pickle.dump(replaced_songs, f)

        self.replaced_songs = replaced_songs

        return
