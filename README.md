# PyRap

Collection of tools built to analyze song lyrics utilizing the Genius API and natural language processing

## Getting Started

In order to get up and running analyzing the sick rhyme schemes of your favorite artists in Python, here are the steps
you have to follow:

First, open a [Genius](https://genius.com/signup) account and follow the [docs](https://docs.genius.com/) to get an
access token for the application. The token will be about 64 characters long with digits, letters, different characters.
Once you have that, paste it into 'settings.py' as the 'access_token' variable. This will be used for making requests to
the Genius API to get artist info and song lyrics.

Once you have your access token setup in 'settings.py', look through the artists already downloaded in the 'Song Lyrics'
folder and see if there are any of your favorites missing. If there are missing artists, open up the 'Main.py' file, uncomment
the line '#Get_Lyrics([artists])' and put in the additional artists you wish to download.

Then to download the additional artists and train and test the NLP model on identifying an artist based on song lyrics, simply run
the 'Main.py' file (default number of artists to test is 10) and the output will be the 1) number of training lyrics 2) number of
 test lyrics 3) number of correct predictions on the test lyrics and 4) the accuracy % of the model. This is a small but interesting
 application of NLP models.

My overall goal for this project is to statistically analyze song lyrics while also improving my own lyric writing abilities.

Be on the look out for my robo-rapper.

## Built With

* [NLTK](http://www.nltk.org/) - Text Analysis
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - JSON/HTML scraping
* [Pandas](http://pandas.pydata.org/) - Data matrix management
* [Scikit-Learn](http://scikit-learn.org/stable/) - NLP modeling