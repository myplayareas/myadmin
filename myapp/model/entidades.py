from json import JSONEncoder

# Define a Classe Usuario
class Usuario:
    # Construtor da classe
    def __init__(self,id, fullname, username, password, image):
        self.id = id
        self.name = fullname
        self.username = username
        self.password = password
        self.image = image

# Classe que converte Objeto em JSON
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    

# Define a Classe Repositorio
class Repositorio:
    def __init__(self, id, name, link, user):
        self.id = id
        self.name = name
        self.link = link
        self.user = user
        self.creation_date = None
        self.analysis_date = None
        self.analysis = 0