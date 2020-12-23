import unittest
from myapp.utils.utilidades import Util, DisplayablePath, MyClone, MyEncoder
import os.path
import git

class TestUtilities(unittest.TestCase):
    def setUp(self):
        self.git_url = "https://github.com/mining-software-repositories/sysrepomsr"
        self.repo_directory = "/Users/armandosoaressousa/testes/sysrepomsr"
        self.path = "/Users/armandosoaressousa/git/sysrepomsr"
        self.repo_directory_temp = "/Users/armandosoaressousa/testes/temp"
        self.repository_name = "sysrepomsr"
        self.displayablePath = DisplayablePath.make_tree("/Users/armandosoaressousa/git/sysrepomsr")
        self.util = Util()
        self.myClone = MyClone(self.repository_name, self.git_url, self.repo_directory)

    # Create an empty file 
    # Check if file exists
    def test_createEmptyFile(self):        
        try: 
            file_test = self.path + "/" + "temp.txt"
            print(file_test)
            self.util.createEmptyFile(file_test)
            self.assertEqual(os.path.isfile(file_test), True) 
        except Exception as e:
            print(e)
            self.fail("Erro ao criar o arquivo {} vazio!".format(file_test))

    def test_showProgressBar(self):
        try: 
            time = 1
            step = 5
            self.util.showProgressBar(time, step)
        except Exception as e:
            print(e)
            self.fail("Erro ao fazer a barra de progresso!")

    def test_list_files(self): 
        try:
            self.util.list_files(self.path)
        except Exception as e:
            print(e)
            self.fail("Erro ao listar os arquivos do diretorio {}".format(self.path))

    def test_listAllFilesFromDirectory(self):
        try:
            self.util.listAllFilesFromDirectory()
        except Exception as e:
            print(e)
            self.fail("Erro ao listar os arquivos do diretorio corrente.")

    def test_listAllDirectoriesAndFilesFromPath(self):        
        try:
            dicionario = self.util.listAllDirectoriesAndFilesFromPath(self.path)
            print('Dicionario: {}'.format(dicionario))
            print('Tamanho do dicionario: {}'.format(len(dicionario)))
        except Exception as e:
            print(e)
            self.fail("Erro ao listar os arquivos e subdiretorios do diretorio {}".format(self.path))

    def test_displayablepath(self):
        try: 
            paths = self.displayablePath
            for path in paths:
                print(path.displayable())
        except Exception as e:
            print(e)
            self.fail("Erro ao listar os arquivos e subdiretorios do diretorio {}".format(self.path))
        
    # Clone a new repository
    def test_git_clone_remote_repository(self):
        try:
            Util.CreateDirectory(self.repo_directory)
            self.myClone.cloning()
            print("O repositorio remoto {} foi criado com sucesso no diretorio {}".format(self.repo_directory,self.git_url))
            self.assertEqual(True, True)
        except Exception as e:
            print(e)
            self.fail("Erro ao clonar o repositorio {} no diretorio corrente")

    # Try to create clone a repository in a directory that already exists
    def test_git_clone_remote_repository_already_exists_directory(self):
        try:
            git.Repo.clone_from(self.git_url, self.repo_directory)
            self.fail("Não deveria permitir o clone do repositorio {} no diretorio {}".format(self.git_url, self.repo_directory))
        except Exception as e:
            print(e)
            self.assertEqual(1,1)    

    def test_run_command(self):
        cmd_cloc = ['cloc', self.path, '--json', '--by-file',  '--report-file=' + self.repository_name +'.json']
        print( str(self.util.run_command(cmd_cloc).stdout, 'utf-8') )