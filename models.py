
class Usuario:
    def __init__(self, apelido, nome, senha, email, data_registro):
        self.apelido = apelido
        self.nome = nome
        self.senha = senha
        self.email = email
        self.data_registro = data_registro

class Log:
    def __init__(self, id, apelido, tipo, data=''):
        self.id = id
        self.apelido = apelido
        self.tipo = tipo
        self.data = data