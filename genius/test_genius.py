import unittest

from genius import get_url
from genius import sort_lyrics

from pdb import set_trace as st


class TestGenius(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_lyrics(self):

        url = 'https://genius.com/Smooky-margielaa-not-right-lyrics'
        lyrics = get_url(url)
        l = sort_lyrics(lyrics)

        if lyrics:
            return
        else:
            return -1


if __name__ == '__main__':
    unittest.main()
