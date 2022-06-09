from models import Usuario, Log
from datetime import datetime

class ReceitasDao():
    def __init__(self, db):
        self.__db = db

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute('SELECT * FROM receitas')
        receitas = traduz_receitas(cursor.fetchall())
        return receitas

    def alterar(self, id, nome, descricao, lista_ingredientes):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'UPDATE receitas SET NOME="{nome}", DESCRICAO="{descricao}", INGREDIENTES="{lista_ingredientes}" WHERE ID={id};')
        self.__db.connection.commit()

    def criar(self, nome, descricao, ingredientes):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'INSERT INTO receitas (NOME, DESCRICAO, INGREDIENTES) VALUES ("{nome}", "{descricao}", "{ingredientes}");')
        self.__db.connection.commit()

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'SELECT * FROM receitas WHERE ID = {id}')
        receita = cria_receita(cursor.fetchone())
        return receita

    def ultimo_id(self):
        cursor = self.__db.connection.cursor()
        cursor.execute("SELECT max(id) FROM receitas LIMIT 1;")
        ID = cursor.fetchone()
        num = int()
        for i in ID:
            if int(i):
                num += i
        return num

    def deletar(self, ID):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'DELETE FROM receitas WHERE ID = {ID}')
        self.__db.connection.commit()

    def get_data_por_id(self,id):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'SELECT DATA_CRIACAO FROM receitas WHERE ID = {id}')
        return cursor.fetchone()

class UsuarioDao():
    def __init__(self, db):
        self.__db = db

    def buscar_por_apelido(self, apelido):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'SELECT * FROM usuarios WHERE APELIDO = "{apelido}"')
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'SELECT * FROM usuarios')
        usuarios = cursor.fetchall()
        return lista_usuario(usuarios)

    def criar(self, apelido, nome, senha, email):
        cursor = self.__db.connection.cursor()
        cursor.execute\
            (f'INSERT INTO usuarios (APELIDO, NOME, SENHA, EMAIL) VALUES ("{apelido}", "{nome}", "{senha}", "{email}");')
        self.__db.connection.commit()

    def remover(self, apelido):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'DELETE FROM usuarios WHERE APELIDO = "{apelido}"')
        self.__db.connection.commit()

class LogDao():
    def __init__(self, db):
        self.__db = db

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'SELECT * FROM db_log')
        logs = cursor.fetchall()
        return lista_logs(logs)

    def adicionar(self, ID, APELIDO, TIPO:str):
        cursor = self.__db.connection.cursor()
        cursor.execute(f'INSERT INTO db_log (ID, APELIDO, TIPO) VALUES ("{ID}", "{APELIDO}", "{TIPO}")')
        self.__db.connection.commit()

def cria_receita(receita):
    def cria_lista(tratar):
        lista = list()
        tratar = tratar.replace('(', '')
        tratar = tratar.replace('[', '')
        tratar = tratar.replace(']', '')
        tratar = tratar.replace("'", "")
        for i in tratar.split(')'):
            i = i.removeprefix(',')
            for c, item in enumerate(i.split(",")):
                if c == 0:
                    quantidade = item
                else:
                    ingrediente = item
                    tupla = (quantidade.strip(), ingrediente.strip())
                    lista.append(tupla)
        return lista
    print(receita[4])
    return {'receitas':
                 {receita[0]: {'nome': receita[1].strip(), 'descricao': receita[2], 'data_criacao': receita[4]}},
            'ingredientes': {receita[0]: list(cria_lista(receita[3]))}}

def traduz_receitas(receitas) -> list:
    return list(map(cria_receita, receitas))

#T0: Apelido, T1: Nome, T2: senha, T3: email, T4: data_registro
def traduz_usuario(tupla) -> Usuario:
    return Usuario(tupla[0], tupla[1], tupla[2], tupla[3], tupla[4])

def lista_usuario(usuarios) -> list:
    return list(map(traduz_usuario, usuarios))

#T0: ID, T1: APELIDO, T2: TIPO, T3: DATA
def lista_logs(logs) -> list:
    def traduz_log(tupla) -> Log:
        return Log(tupla[0], tupla[1], tupla[2], tupla[3])
    return list(map(traduz_log, logs))

if __name__ == '__main__':
    '''
    #0=ID 1=NOME 2=DESCRIÇÂO 3=Ingredientes
    print('Conectando...')
    conn = MySQLdb.connect(user='root', passwd='root1', host='localhost', port=3306)
    conn.cursor().execute('USE site_receitas;')
    cursor = conn.cursor()
    cursor.execute('select * from receitas')
    print('___RECEITAS___')


    print('Dados 1 ')
    for item in dados['receitas']:
        print(dados['receitas'][item].keys())
        print(f'Nome: {dados["receitas"][item]["nome"]} ')
        print(f'Descrição: {dados["receitas"][item]["descricao"]} ')
        print(f'Ingredientes: {dados["receitas"][item]["ingredientes"]}')
        print()
    
    '''
