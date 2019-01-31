import requests
from bs4 import BeautifulSoup as BS

import settings

token = 'Bearer ' + settings.access_token
base_url = "http://api.genius.com"
headers = {'Authorization': token}


def get_url(url):
    '''
    Get Lyrics for a song given the Genius Web URL
    '''
    page = requests.get(url)
    html = BS(page.text, "html.parser")
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics


def sort_lyrics(lyrics):
    '''
    Sort Lyrics into different sections
    '''
    lines = lyrics.splitlines()
    sections = {}
    sec_ind = []

    for i in range(0, len(lines)):

        line = lines[i]

        if ']' in line and '[' in line:
            s_ind = i
            sec_ind.append(s_ind)

    sec_ind = sorted(sec_ind)

    for i in range(0, len(sec_ind)-1):

        ind = sec_ind[i]
        line = lines[ind]

        sec = line.replace('[', '').replace(']', '').lower()

        sec_lines = lines[ind + 1:sec_ind[i+1]]
        sec_lines = [x for x in sec_lines if x != '']

        sections[sec] = sec_lines

    return sections


def get_lyrics(url):
    '''
    Print Lyrics from genius page URL
    '''
    lyrics = get_url(url)
    sorted_lyrics = sort_lyrics(lyrics)

    return sorted_lyrics
