#Teste clone git repository
import time
import git
from git import RemoteProgress
import os
from subprocess import Popen, PIPE, STDOUT
from time import sleep
from tqdm import tqdm
from json import JSONEncoder
import shutil
import subprocess
from subprocess import Popen, PIPE, STDOUT
import json

# Classe que converte Objeto em JSON
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    

class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print('update', op_code, cur_count, max_count, message)

class MyClone: 
    def __init__(self, repository_name, git_remote, git_root):
        self.repository = repository_name
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

    # path = "/Users/armandosoaressousa/git/myadmin"
    @staticmethod
    def listAllDirectoriesAndFilesFromPath(path):        
        dictionary_directory_files = {}
        for dirpath, dirnames, filenames in os.walk(path):
            directory_level = dirpath.replace(path, "")
            directory_level = directory_level.count(os.sep)
            list_level_and_files = []
            list_files = []
            for f in filenames:
                if not f.startswith("."):
                    list_files.append(f)
            if (not "." in dirpath) and ("__" not in dirpath):
                list_level_and_files.append(directory_level)
                list_level_and_files.append(list_files)
                dictionary_directory_files[dirpath] = list_level_and_files
        return dictionary_directory_files
    # More detaisl in https://janakiev.com/blog/python-filesystem-analysis/

    @staticmethod
    def CreateDirectoryIfNotExists(path):
        if not os.path.exists(path):
            os.makedirs(path)

    @staticmethod
    def CreateDirectory(path):
        if os.path.exists(path):
            # Remove the folder completelly
            shutil.rmtree(path, ignore_errors=True)
            # Create the new folder
            os.makedirs(path)

    @staticmethod
    def DeleteFileIfExist(path):
        if os.path.exists(path):
            os.remove(path)
        else:
            print("The file does not exist")


    @staticmethod
    def run_command(cmd, check=False, timeout=30, shell=False, log=None):
        try:
            proc = subprocess.Popen(cmd, shell=shell, start_new_session=True, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
            proc_stdout, proc_stderr = proc.communicate()
        except subprocess.TimeoutExpired as e:
            os.killpg(proc.pid, -9)
            
        completed = subprocess.CompletedProcess(args=cmd,returncode=proc.returncode,stdout=proc_stdout,stderr=proc_stderr)

        if check and proc.returncode != 0:
            print(f"{completed.args}, {completed.stdout}, {completed.stderr},{completed.returncode}")

        return completed 

    @staticmethod
    def save_dictionary_in_json_file(name, user_id, my_dictionary, my_type): 
        try: 
            # Save my_dictionary in a json file
            singleName = name + "_" + my_type + ".json"
            user_directory = Constant.PATH_JSON + '/' + str(user_id)
            fileName = user_directory + '/' + singleName
            #Create the user directory if not existe
            Util.CreateDirectoryIfNotExists(user_directory)
            with open(fileName, 'w', encoding="utf-8") as jsonFile:
                json.dump(my_dictionary, jsonFile)
            print("The file {} was saved with success!".format( singleName ))
        except: 
            print( "Error when try to save the json file")



from pathlib import Path

#https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
class DisplayablePath(object):
    display_filename_prefix_middle = '├──'
    display_filename_prefix_last = '└──'
    display_parent_prefix_middle = '    '
    display_parent_prefix_last = '│   '

    def __init__(self, path, parent_path, is_last):
        self.path = Path(str(path))
        self.parent = parent_path
        self.is_last = is_last
        if self.parent:
            self.depth = self.parent.depth + 1
        else:
            self.depth = 0

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    @classmethod
    def make_tree(cls, root, parent=None, is_last=False, criteria=None):
        root = Path(str(root))
        criteria = criteria or cls._default_criteria

        displayable_root = cls(root, parent, is_last)
        yield displayable_root

        children = sorted(list(path
                               for path in root.iterdir()
                               if criteria(path)),
                          key=lambda s: str(s).lower())
        count = 1
        for path in children:
            is_last = count == len(children)
            if path.is_dir():
                yield from cls.make_tree(path,
                                         parent=displayable_root,
                                         is_last=is_last,
                                         criteria=criteria)
            else:
                yield cls(path, displayable_root, is_last)
            count += 1

    @classmethod
    def _default_criteria(cls, path):
        return True

    @property
    def displayname(self):
        if self.path.is_dir():
            return self.path.name + '/'
        return self.path.name

    def displayable(self):
        if self.parent is None:
            return self.displayname

        _filename_prefix = (self.display_filename_prefix_last
                            if self.is_last
                            else self.display_filename_prefix_middle)

        parts = ['{!s} {!s}'.format(_filename_prefix,
                                    self.displayname)]

        parent = self.parent
        while parent and parent.parent is not None:
            parts.append(self.display_parent_prefix_middle
                         if parent.is_last
                         else self.display_parent_prefix_last)
            parent = parent.parent

        return ''.join(reversed(parts))

#paths = DisplayablePath.make_tree(Path('doc'))
#for path in paths:
#    print(path.displayable())

class Constant:
    PATH_MYADMIN = os.path.abspath(os.getcwd())
    PATH_MYAPP = PATH_MYADMIN + '/myapp'
    PATH_STATIC = PATH_MYADMIN + '/myapp/static'
    PATH_IMG = PATH_MYADMIN + '/myapp/static/img'
    PATH_JSON = PATH_MYADMIN + '/myapp/static/json'
    PATH_UPLOADS = PATH_MYADMIN + '/myapp/static/uploads'

#git_remote = 'https://github.com/armandossrecife/sysdemo.git'
#git_root = '/Users/armandosoaressousa/git/myadmin/temp/sysdemo'