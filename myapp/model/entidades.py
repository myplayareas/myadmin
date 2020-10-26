from json import JSONEncoder

# Define a Classe Usuario
class Usuario:
    id = 0
    name = ''
    username = ''
    password = ''
    image = ''

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
    id = 0
    name = ''
    link = ''

    def __init__(self, id, name, link):
        self.id = id
        self.name = name
        self.link = link