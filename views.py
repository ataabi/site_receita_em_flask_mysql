from flask import render_template, request, redirect, url_for, session, flash, send_from_directory
from main import procura_receita
from dao import ReceitasDao, UsuarioDao, LogDao
from app import db, app
from datetime import datetime, timedelta
import os

receita_dao = ReceitasDao(db)
usuario_dao = UsuarioDao(db)
logs_dao = LogDao(db)

@app.route('/')
def index():
    dados = receita_dao.listar()
    temp = list()
    num_receitas = len(dados)
    num_paginas = round(num_receitas/4)

    #Pega os itens que seram exibidos na página
    for i in range(4):
        temp.append(dados[i])

    return render_template('receitas.html', dados=temp, num_paginas=num_paginas)

@app.route('/<int:pag>')
def paginacao(pag):
    dados = receita_dao.listar()
    temp = list()
    min_receitas = (pag * 4)-4
    max_receitas = pag * 4
    num_receitas = len(dados)
    num_paginas = round(num_receitas / 4)

    for i in range(min_receitas, max_receitas ):
        try:
            temp.append(dados[i])
        except:
            pass

    return render_template('paginas.html', dados=temp, num_paginas=num_paginas)

@app.route('/receita/<int:id>')
def receita(id):
    receita = receita_dao.busca_por_id(id)
    return render_template('receita.html', receita=receita, id=id)

@app.route('/buscador', methods=['POST','GET'])
def buscador():
    dados = receita_dao.listar()

    if not 'radio_pesquisa' in request.form:
        tipo_busca = 0
    else:
        tipo_busca = int(request.form['radio_pesquisa'])

    # Pegando os valores da url e transformando em uma lista
    if request.form['buscar']:
        lista_de_busca = request.form['buscar'].strip().split(',')
        # Sanitizando e procurando os correspondentes
        resultado = procura_receita(dados, lista_de_busca, tipo_busca)
        return render_template('pesquisa.html', dados=dados, resultado=resultado)
    else:
        return render_template('pesquisa.html')

@app.route('/adicionar', methods=['GET', 'POST'])
def adicionar_receita():
    print(request.method)
    # verifica se há um usuario logado
    if not 'nome_usuario' in session or session['nome_usuario'] == False:
            return redirect(url_for('login', proxima=url_for('adicionar_receita')))

    # Adiciona ou remove o numero de linha na pagina Adicionar Receitas
    if request.method == 'POST':
        adi = request.form.get("adicionar_ingrediente")
        rem = request.form.get("remover_ingrediente")

        if adi:
            session['numero_ingredientes'] += 1
        elif rem:
            if session['numero_ingredientes'] <= 1:
                session['numero_ingredientes'] == 1
            else:
                session['numero_ingredientes'] -= 1

    # verifica se a session ja foi criada
    if request.method == 'GET':
        if 'numero_ingredientes' not in session:
            session['numero_ingredientes'] = 1

    return render_template('adicionar.html', n_ing=session['numero_ingredientes'])

@app.route('/criar_receita', methods=['POST'])
def criar_receita():
    nome = request.form['nome'].strip()
    ingredientes = []
    descricao = request.form['descricao']

    for n in range(session['numero_ingredientes']):
        ingrediente = request.form[f'ingrediente{n}'].strip()
        print('Ingrediente:',ingrediente)
        quantidade = request.form[f'quantidade{n}'].strip()
        print('Quantidade :',quantidade)
        ingredientes.append((quantidade, ingrediente))

    receita_dao.criar(nome, descricao, str(ingredientes))
    ID = receita_dao.ultimo_id()
    apelido = session['apelido_usuario']
    logs_dao.adicionar(ID, apelido, 'CRIADO')
    print(ID)
    uploads_path = app.config['UPLOADS_PATH']
    arquivo = request.files['imagem']
    arquivo.save(f'{uploads_path}/{nome}_{ID}.jpg')

    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST','GET'])
def editar_receita(id):
    dados = receita_dao.busca_por_id(id)
    receita = dados['receitas'][id]
    ingredientes = dados['ingredientes'][id]

    # Adiciona ou remove o numero de linha na pagina Adicionar Receitas
    if request.method == 'POST':
        adi = request.form.get("adicionar_ingrediente")
        rem = request.form.get("remover_ingrediente")

        if adi:
            session['numero_ingredientes'] += 1
        elif rem:
            if session['numero_ingredientes'] <= 1:
                session['numero_ingredientes'] == 1
            else:
                session['numero_ingredientes'] -= 1

    # verifica se a session ja foi criada
    if request.method == 'GET':
        if 'numero_ingredientes' not in session or \
            session['numero_ingredientes'] != len(dados['ingredientes'][id]):
            session['numero_ingredientes'] = len(dados['ingredientes'][id])

    return render_template('editar_receita.html',
                           receita=receita,
                           ingredientes=ingredientes,
                           id=id,
                           n_ing=session['numero_ingredientes'])

@app.route('/alterar_receita', methods=['POST'])
def alterar_receita():

    uploads_path = app.config['UPLOADS_PATH']
    ingredientes = []

    nome = request.form['nome'].strip().title()
    descricao = request.form['descricao']
    id = request.form['id']

    for n in range(session['numero_ingredientes']):
        ingrediente = request.form[f'ingrediente{n}'].strip().title()
        quantidade = request.form[f'quantidade{n}'].strip().title()
        ingredientes.append((quantidade, ingrediente))

    receita_dao.alterar(id,nome,descricao,str(ingredientes))
    logs_dao.adicionar(id, session['apelido_usuario'], 'ALTERADO')

    nome_img = recupera_imagem(id)
    arquivo = request.files['imagem']
    arquivo.save(f'{uploads_path}/{nome_img}')

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):

    receita_dao.deletar(id)
    deleta_arquivo(id)

    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')

    if not 'nome_usuario' in session or session['nome_usuario'] == False:
        if proxima is None:
            print(f'rota sem nd')
            return render_template('login.html')
        print(f'se nao logado com proxima')
        return render_template('login.html', proxima=proxima)
    else:
        print(f"você já está logado como {session['nome_usuario']}")
        return render_template('login.html', usuario=session['nome_usuario'])

@app.route('/logout')
def logout():
    session['nome_usuario'] = False
    session['apelido_usuario'] = False
    return redirect(url_for('index'))

@app.route('/autenticar', methods=['POST'])
def autenticar():
    nome = request.form['nome_usuario']
    senha = request.form['senha_usuario']

    if nome == 'ADMIN0' and senha == 'loveflask':
        return redirect(url_for('admin'))

    def valida_usuario(nome,senha):
        usuario = usuario_dao.buscar_por_apelido(nome)
        if usuario:
            if usuario.apelido == nome and usuario.senha == senha:
                return True

    if valida_usuario(nome, senha):
        usuario = usuario_dao.buscar_por_apelido(nome)
        session['nome_usuario'] = usuario.nome
        session['apelido_usuario'] = usuario.apelido
        flash(f'{usuario.nome} logado com sucesso')
        if request.form['proxima']:
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        return redirect(url_for('index'))

    return redirect(url_for('login'))

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    apelido = request.form['u_apelido']
    nome = request.form['u_nome']
    senha = request.form['u_senha']
    email = request.form['u_email']

    usuario_dao.criar(apelido, nome, senha, email)

    return redirect(url_for('login'))

@app.route('rem_usuario/<int:ind>', methods=['POST',])
def rem_usuario(id):
    usuario_dao.remover(id)
    return redirect(url_for('admin'))

@app.route('/adimin')
def admin():
    receitas = receita_dao.listar()
    usuarios = usuario_dao.listar()
    logs = logs_dao.listar()
    return render_template('admin.html', receitas=receitas, usuarios=usuarios, logs=logs)

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOADS_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo

def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    if arquivo:
        os.remove(os.path.join(app.config['UPLOADS_PATH'], arquivo))

def registra_log(id,apelido):
    pass
