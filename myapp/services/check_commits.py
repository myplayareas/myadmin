import datetime
from pydriller import Repository
from collections import Counter
from wordcloud import WordCloud
from myapp.utils.utilidades import Util
import matplotlib.pyplot as plt
from myapp.utils.utilidades import Constant

# Class to analysis all commits from a branch of git repository
class CheckCommits:
    # constructor pass the path of repository
    def __init__(self, repository, name):
        self.repository = repository
        self.name = name
    
    # List all Commits from Authors
    # return a dictionary like this: hash, author, date, list of files in commit
    # dictionary = {'hash': ['author', 'date of commit', [file1, file2, ...]]}
    def dictionaryWithAllCommmits(self):
        dictionaryAux = {}
        for commit in Repository(self.repository).traverse_commits():
            commitAuthorNameFormatted = '{}'.format(commit.author.name)
            commitAuthorDateFormatted = '{}'.format(commit.author_date)
            listFilesModifiedInCommit = []
            for modification in commit.modified_files:
                itemMofied = '{}'.format(modification.filename)
                listFilesModifiedInCommit.append(itemMofied)
            dictionaryAux[commit.hash] = [commitAuthorNameFormatted, commitAuthorDateFormatted, listFilesModifiedInCommit] 
        return dictionaryAux

    # Return a Counter with frequency of each file analysed
    # The Counter like this:
    # Counter({file1: frequency of file1, file2: frequence of file2, ...})
    def counterWithFrequencyOfFile(self):
        listFull = []
        for key, value in self.dictionaryWithAllCommmits().items():
            listAxu = []
            listAxu = value[2]
            for eachItem in listAxu:
                listFull.append(eachItem)
        return Counter(listFull)

    # Generate a Word of Cloud about each file according frequence
    def generateWordCloud(self, user_id):
        dictionaryOfFileFrequence = self.counterWithFrequencyOfFile()
        wordcloud = WordCloud(width = 1200, height = 1000, random_state=1, background_color='black', colormap='Set2', collocations=False)
        wordcloud.generate_from_frequencies(frequencies=dictionaryOfFileFrequence)
        # Display the generated image:
        user_directory = Constant.PATH_IMG + "/" + str(user_id)
        path_to_save =  user_directory + "/"
        fileName = path_to_save + self.name + ".png"
        #Create the user directory if not existe
        Util.CreateDirectoryIfNotExists(user_directory)
        wordcloud.to_file(fileName)