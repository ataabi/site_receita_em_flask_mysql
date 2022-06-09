from models import Usuario
from flask import Flask
from flask_mysqldb import MySQL
from dao import ReceitasDao

'''
# Criando Receitas de Teste
bolo = ['Ovo', 'Leite', 'Trigo', 'Áçucar', 'Fermento']
ovo_frito = ['Ovo']
ovo_mexido = ['Ovo', 'Manteiga']
macarrao_vermelho = ['Macarrão', 'Molho De Tomate']
macarrao_branco = ['Macarrão', 'Nós Noscada', 'Leite', 'Manteiga', 'Trigo', 'Sal']

receita_bolo = Receita(1,'Bolo Branco', bolo, ' t ')
receita_ovo_frito = Receita(2,'Ovo Frito', ovo_frito, ' t ')
receita_ovo_mexido = Receita(3,'Ovo Mexido', ovo_mexido, ' t ')
receita_macarrao_vermelho = Receita(4,'Macarrão ao Molho Vermelho', macarrao_vermelho, ' t ')
receita_macarrao_branco = Receita(5,'Macarrão ao Molho Branco', macarrao_branco, ' t ')

receitas = [receita_macarrao_branco, receita_macarrao_vermelho,
            receita_bolo, receita_ovo_frito, receita_ovo_mexido]
'''

dados = {
    'receitas': {
        0: {"nome": "Bolo Branco", "descricao": "Junte todos os ingredientes, bata na batedeira e leve ao "
                                                          "forno por 40m"},
        1: {"nome": "Ovo Mexido", "descricao": "Coloque a manteiga na frigideira, depois adicione o ovo e "
                                                          "mexa até estar no ponto"},
        2: {"nome": "Ovo Frito", "descricao": "Em uma frigideira bem quente quebre o ovo"},
        3: {"nome": "Macarrão ao Molho Vermelho", 'descricao': "Ferva o macarrão e adicione molho de tomate"},
        4: {"nome": "Macarrão ao Molho Branco", "descricao": "Ferva o macarrão, Molho: Adicione o aquece o leite,"
                                                              "adicione o trigo aos poucos, depois sal, nós noscada"
                                                              "e pimenta a gosto."}
    },
    "ingredientes": {
        0: [('1 un', 'ovo'), ('1/2 x', 'leite'), ('2x', 'trigo'), ('1x', 'áçucar'), ('1c', 'fermento')],
        1: [('1 un', 'ovo')],
        2: [('1 un', 'ovo'), ('1/2 c', 'manteiga')],
        3: [('500 g', 'macarrão'), ('300g','molho de tomate'), ('Pitada','sal')],
        4: [('500 g', 'macarrão'), ('1 1/2x', 'leite'), ('1 c','trigo'), ('2g','nós noscada'), ('A gosto','sal')]
    }
}
'''
Medidas
un = unidade
c = colher
cc = colher de café
ml = ml
x = xicará
'''

# Instanciando um usuario
usuario1 = Usuario('tsukashi','jhony','loveflask','email@email.com','')

lista_usuario = [usuario1]

def sanitiza_lista(lista_ingredientes):
    tempo = []
    for ingredientes in lista_ingredientes:
        tempo.append(ingredientes.strip().lower())
    return sorted(tempo)

# Verificando se tem os ingredientes
def procura_receita(receitas, lista_de_busca, tipo_pesquisa=0):
    '''
    :param lista_de_busa: lista com os ingredientes a procurar
    :param tipo_pesquisa: 0 procura se comtem o ingrediente,
        1 procura se comtem somente o ingrediente
    :return: Set com os ID das receitas encontradas
    '''

    encontrados = set()
    lista_de_busca = sanitiza_lista(lista_de_busca)

    if tipo_pesquisa == 0:
        for receita in receitas:
            # print('Procura se contem')
            for ID in receita['ingredientes']:
                for lista in receita['ingredientes'][ID]:
                    # print(ID, lista[1])
                    for ing in lista_de_busca:
                        # print(ing)
                        if ing == lista[1].lower().strip():
                            # print(f'Math ID{ID}')
                            encontrados.add(ID)

    if tipo_pesquisa == 1:
        # print('Procura somente')

        lista_de_comparacao = []

        for receita in receitas:
            for ID in receita['ingredientes']:
                print(f'ID: {ID}, LEN: {len(receita["ingredientes"][ID])}')
                for lista in receita['ingredientes'][ID]:
                    for ing in lista_de_busca:
                        if ing == lista[1].lower():
                            lista_de_comparacao.append(lista[1].lower())
                print(lista_de_comparacao)
                print(lista_de_busca)
                if sorted(lista_de_comparacao) == lista_de_busca \
                        and len(lista_de_busca) == len(receita["ingredientes"][ID]):
                    encontrados.add(ID)
                lista_de_comparacao.clear()
            # print(f'Encontrados: {encontrados}')

    return encontrados

def verifica_usuario(session):
    # se o usuario NÂO ESTIVER logado return True
    if not 'nome_usuario' in session or session['nome_usuario'] == False:
        return False
    else:
        return True


if __name__ == '__main__':
    app = Flask(__name__)
    app.secret_key = 'ChaveSuperSecreta'
    db = MySQL(app)
    receita_dao = ReceitasDao(db)
    dados = receita_dao.listar()
    lista = ['ovo']
    tipo = 0
    resultado = procura_receita(dados, lista, tipo)
    print(resultado)


