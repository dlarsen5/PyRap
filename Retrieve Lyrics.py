import requests
from bs4 import BeautifulSoup as BS
import pickle
import settings
import logging
import os
import time

def lyrics_from_song_api_path(song_api_path):

    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BS(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

def construct_lyrics(song_title,artist_name):
    search_url = base_url + "/search?q=" + song_title
    response = requests.get(search_url, headers=headers)
    json = response.json()
    song_info = None
    for hit in json['response']['hits']:
      if hit['result']['primary_artist']['name'] == artist_name:
        song_info = hit
        break
    if song_info:
      song_api_path = song_info['result']['api_path']
      return lyrics_from_song_api_path(song_api_path)

def get_artist_songs(artist):
    artist_id = ''
    search_url = base_url + "/search?q=" + artist
    response = requests.get(search_url, headers=headers)
    json = response.json()

    for hit in json['response']['hits']:
        if hit['result']['primary_artist']['name'] == artist:
            artist_id = hit['result']['primary_artist']['api_path']
            break

    artist_url = base_url + artist_id + '/songs?sort=popularity&per_page=%s' % settings.number_of_songs
    artist_response = requests.get(artist_url, headers=headers)
    artist_json = artist_response.json()

    song_paths = {}
    song_lyrics = {}

    for song in artist_json['response']['songs']:
        song_paths[song['title_with_featured']] = song['api_path']

    for song,song_path in song_paths.items():
        song_lyrics[song] = lyrics_from_song_api_path(song_path)

    return song_lyrics

if __name__ == '__main__':

    token = 'Bearer ' + settings.access_token
    base_url = "http://api.genius.com"
    headers = {'Authorization': token}

    log_file = 'Logs/run.log'

    if os.path.exists(log_file):
        os.remove(log_file)

    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    logging.getLogger('requests').setLevel(logging.CRITICAL)

    logging.info('Starting at %s' % time.time())

    for artist in settings.artists_to_download:

        artist_path = 'Song Lyrics/' + artist.replace(' ', '_')

        if not os.path.exists(artist_path):

            try:
                songs = get_artist_songs(artist)
                with open(artist_path, 'wb') as file:
                    pickle.dump(songs, file)
                logging.info('Got %s' % artist)

            except Exception as e:
                logging.error('Error with %s: %s' % (artist,e))

        else:
            logging.error('%s already downloaded' % artist)

    logging.info('Ended at %s' % time.time())