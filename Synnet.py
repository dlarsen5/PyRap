import requests
from nltk.corpus import wordnet as wn
import nltk
from Model import Artist_DataFrame


artists = ['Kendrick Lamar','Drake','Chance The Rapper','J. Cole','Logic','Future','Chief Keef','Eminem','Kanye West','JAY-Z','Big Sean',
                      'Lil Uzi Vert','Tyler, The Creator','Earl Sweatshirt','2 Chainz','G-Eazy','ScHoolboy Q','Young Thug','Joey Bada$$', 'PnB Rock',
                      'Flatbush Zombies','A$AP Rocky','A$AP Ferg','Dumbfoundead','Tory Lanez','Waka Flocka Flame','Nas','A Tribe Called Quest','Vic Mensa',
                      '$UICIDEBOY$','Denzel Curry','Maxo Kream','Isaiah Rashad','Mike Stud','Mac Miller','Yonas','Childish Gambino','Rich Chigga',
                      'Three 6 Mafia','Azizi Gibson','RiFF RAFF','Lil Dicky','Lil Wayne','Tyga','Gucci Mane','Rick Ross','Asher Roth','Travis Scott','Migos','Rihanna',
                      'Bryson Tiller','21 Savage','Rae Sremmurd','French Montana','Miley Cyrus','XXXTENTACION','Lil Pump','Ski Mask the Slump God','Xavier Wulf',
                      'SmokePurpp','A Boogie Wit Da Hoodie','Playboi Carti','Ugly God','Wiz Khalifa','Justin Bieber','Beyoncé','Nicki Minaj','Meek Mill']

id = wn.synsets('dog')[0].pos() + '0' + str(wn.synsets('dog')[0].offset())

def get_images(id):

    api_url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=%s' % id
    response = requests.get(api_url)

    return

def pos_tagging(corpus):

    tagged_sentences = []

    for sent in corpus:
        tagged_sentences.append(nltk.pos_tag_sents())


text = nltk.word_tokenize(str(Artist_DataFrame(['SmokePurpp','A Boogie Wit Da Hoodie'])['Lyrics'][10].values))

print(nltk.pos_tag(text))