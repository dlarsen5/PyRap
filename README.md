# PyRap

Collection of tools built to analyze song lyrics utilizing the Genius API and natural language processing

## Getting Started

In order to get up and running analyzing the sick rhyme schemes of your favorite artists in Python, here are the steps
you have to follow:

First, open a [Genius](https://genius.com/signup) account and follow the [docs](https://docs.genius.com/) to get an
access token for the application. The token will be about 64 characters long with digits, letters, different characters.
Once you have that, paste it into 'settings.py' as the 'access_token' variable. This will be used for making requests to
the Genius API to get artist info and song lyrics.

Next in 'settings.py', list artists you wish to download song lyrics for in the 'artists_to_download' list variable. Then
run 'Retrieve Lyrics.py' to download the lyrics for all of the artists you listed in 'settings.py'. This script will
download the top 30 songs from each artist you mention (you can change the number of tracks in 'settings.py' as well defined
by 'number_of_songs') and save them as pickle objects in 'Song Lyrics/' for later analysis. A number of artists' songs and song
lyrics are already included.

Once you have your artist's songs and song lyrics downloaded, run 'Lyric Analysis.py' to analyze the word usage of the artists
using the Python natural language processing library NLTK. This will compute the top 10 words longer than 3 characters (to get rid of excess 'the' and 'a' words) as well as the amount of small words used (less than 3 characters) as well as the total amount of lyrics used in all of an artist's songs. This will then save the statistics as a CSV file called statistics.csv for more detailed analysis.

And that's it (for now). Later on I'll be looking at detailed lyric analysis, including classifying a song as a specific
genre based on the text lyrics and sentiment analysis of individual artists.

My overall goal for this project is to statistically analyze song lyrics while also improving my own lyric writing abilities.

Be on the look out for my robo-rapper.

## Built With

* [NLTK](http://www.nltk.org/) - Text Analysis
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - JSON/HTML scraping
* [Pandas](http://pandas.pydata.org/) - Data matrix management
