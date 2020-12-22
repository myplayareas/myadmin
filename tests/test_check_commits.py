import unittest
from myapp.utils.utilidades import Util, DisplayablePath, MyClone, MyEncoder
import os.path
import git
from myapp.services.check_commits import CheckCommits

class TestCheckCommits(unittest.TestCase):
    def setUp(self):
        self.git_url = "https://github.com/mining-software-repositories/sysrepomsr"
        self.repo_directory = "/Users/armandosoaressousa/testes/sysrepomsr"
        self.repository_name = "sysrepomsr"
        self.checkCommits = CheckCommits(self.repo_directory, self.repository_name)
        self.myClone = MyClone(self.repository_name, self.git_url, self.repo_directory)

    def test_dictionaryWithAllCommmits(self):
        try:
            # Clonning repository in local directory to hurry up
            Util.CreateDirectory(self.repo_directory)
            self.myClone.cloning()
            print("O repositorio remoto {} foi criado com sucesso no diretorio {}".format(self.repo_directory,self.git_url))
            
            allCommits = self.checkCommits.dictionaryWithAllCommmits()
            print(allCommits)
            self.assertEqual(1,1)
        except Exception as e:
            print(e)
            self.fail("Erro ao gerar todos os commits do repositorio {}".format(self.repo_directory))

    def test_counterWithFrequencyOfFile(self):
        try: 
            print("Processing the frequency of each file in commits...")
            frequencyOfEachFile = self.checkCommits.counterWithFrequencyOfFile()
            print(frequencyOfEachFile)
            self.assertEqual(1,1)
        except Exception as e:
            print(e)
            self.fail("Error in checkCommits.counterWithFrequencyOfFile()")

    def test_generateWordCloud(self):
        try:
            self.checkCommits.generateWordCloud(1)
            print("The wordcloud was generated with success!")
            self.assertEqual(1,1)
        except Exception as e:
            print(e)
            self.fail("Error in checkCommits.generateWordCloud()")
