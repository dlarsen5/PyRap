from Model import Train_And_Test
from Retrieve_Lyrics import Get_Lyrics


if __name__ == '__main__':

    #Download any artists not already in 'Song Lyrics' folder

    Get_Lyrics(['Justin Bieber'])

    #train and test model using artists' songs in 'Song Lyrics' folder
    #input is number of artists to pull from 'Song Lyrics' folder and input to NLP model

    #to set
    Train_And_Test(number_of_artists=10)