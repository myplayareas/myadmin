#Teste clone git repository
import time
import git
from git import RemoteProgress
import os
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from tqdm import tqdm

class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print('update', op_code, cur_count, max_count, message)

class MyClone: 
    def __init__(self, repository_name, git_remote, git_root):
        self.repository = repository
        self.git_remote = git_remote
        self.git_root = git_root
    
    def cloning(self):
        print('Cloning into %s' % self.git_root, end="", flush=True)
        git.Repo.clone_from(self.git_remote, self.git_root, progress=Progress())

class MyCloneByProcess:
    def __init__(self, git_remote):
        self.git_remote = git_remote
    
    def cloning(self):
        proc = Popen(
            ["git", "clone", git_remote],
            stdout=PIPE, stderr=STDOUT, shell=True
        )

        #stdout, stderr = proc.communicate()
        for line in proc.stdout:
            if line:
                print(line.strip())  # Now you get all terminal clone output text

class Util:
    @staticmethod
    def createEmptyFile(path):
        with open(path, 'a') as file:
            os.utime(path, None)
        return file

    @staticmethod
    def showProgressBar(time, step):
        for i in tqdm(range(step)):
            sleep(time)

    @staticmethod
    def list_files(startpath):
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))

    @staticmethod
    def listAllFilesFromDirectory():
        start_path = '.' # current directory

        for path,dirs,files in os.walk(start_path):
            for filename in files:
                print( os.path.join(path,filename) )

#git_remote = 'https://github.com/armandossrecife/sysdemo.git'
#git_root = '/Users/armandosoaressousa/git/myadmin/temp/sysdemo'