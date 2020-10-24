from json import JSONEncoder

# Define a Classe Usuario
class Usuario:
    id = 0
    nome_completo = ''
    username = ''
    password = ''
    imagem = ''

    # Construtor da classe
    def __init__(self,id, fullname, username,password, image):
        self.id = id
        self.nome_completo = fullname
        self.username = username
        self.password = password
        self.imagem = image

# Classe que converte Objeto em JSON
class MyEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__    