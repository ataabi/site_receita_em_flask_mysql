import MySQLdb
print('Conectando...')
conn = MySQLdb.connect(user='root', passwd='root1', host='localhost', port=3306)


conn.cursor().execute('drop schema site_receitas;')

conn.cursor().execute('CREATE DATABASE site_receitas;')
print('DATABASE site_receitas Criado com sucesso')

conn.cursor().execute('USE site_receitas;')
print('USANDO site_receitas')

conn.cursor().execute('''CREATE TABLE receitas (
    ID INT NOT NULL AUTO_INCREMENT,
    NOME VARCHAR(50) NOT NULL,
    DESCRICAO TEXT,
    INGREDIENTES TEXT,
    DATA_CRIACAO DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(ID)
    )ENGINE=InnoDB;''')
print('Criando Tabela de Receitas')

conn.cursor().execute('''CREATE TABLE `usuarios` (
    APELIDO varchar(20) NOT NULL PRIMARY KEY,
    NOME varchar(20) NOT NULL,
    SENHA varchar(12) NOT NULL,
    EMAIL varchar(25) NOT NULL,
    DATA_REGISTRO DATETIME DEFAULT CURRENT_TIMESTAMP
    )ENGINE=InnoDB;''')
print('Criando Tabela de Usuario')

conn.cursor().execute('''CREATE TABLE DB_LOG(
    ID INT, 
    APELIDO varchar(20),
    TIPO varchar(12),
    DATA DATETIME DEFAULT CURRENT_TIMESTAMP, 
    FOREIGN KEY (ID) REFERENCES receitas(ID),
    FOREIGN KEY (APELIDO) REFERENCES usuarios(APELIDO));''')
print('Criando Tabela de Log')


#Adicionando valores

cursor = conn.cursor()

# Adicionando as Receitas
cursor.executemany(
    'INSERT INTO receitas (NOME, DESCRICAO, INGREDIENTES) VALUES (%s, %s, %s)',
    [{"ID":1, "NOME":"Bolo Branco",
 "DESCRICAO":"Junte todos os ingredientes, bata na batedeira e leve ao forno por 40m",
 "INGREDIENTES":"[('1 un', 'ovo'), ('1/2 x', 'leite'), ('2x', 'trigo'), ('1x', '\u00e1\u00e7ucar'), ('1c', 'fermento')]",
 "DATA_CRIACAO":"2022-05-20 16:04:14"},
 {"ID":2, "NOME":"Ovo Mexido",
  "DESCRICAO":"Coloque a manteiga na frigideira, depois adicione o ovo e mexa at\u00e9 estar no ponto",
  "INGREDIENTES":"[('1 Un', 'Ovo'), ('2 Un', 'Ovo'), ('2 Un', 'Ovo')]",
  "DATA_CRIACAO":"2022-05-20 16:04:14"},
 {"ID":3, "NOME":"Bolo De  Ovo",
  "DESCRICAO":"cozinhe no microndas 2",
  "INGREDIENTES":"[('1 Un', 'Ovo')]",
  "DATA_CRIACAO":"2022-05-20 16:04:14"},
 {"ID":4, "NOME":"Macarr\u00e3o ao Molho Vermelho",
  "DESCRICAO":"Ferva o macarr\u00e3o e adicione molho de tomate",
  "INGREDIENTES":"[('500 g', 'macarr\u00e3o'), ('300g','molho de tomate'), ('Pitada','sal')]",
  "DATA_CRIACAO":"2022-05-20 16:04:14"},
 {"ID":5, "NOME":"Macarr\u00e3o Ao Molho Branco",
  "DESCRICAO":"Ferva o macarr\u00e3o, Molho: Adicione o aquece o leite, adicione o trigo aos poucos, depois sal, n\u00f3s noscada e pimenta a gosto.",
  "INGREDIENTES":"[('500 G', 'Macarr\u00e3o'), ('1 1/2X', 'Leite'), ('1 C', 'Trigo'), ('2G', 'N\u00f3s Noscada'), ('A Gosto', 'Sal')]",
  "DATA_CRIACAO":"2022-05-20 16:04:14"},
 {"ID":6, "NOME":"Bolo De Caneca",
  "DESCRICAO":"Misture tudo e leve ao microondas por 3 minutos",
  "INGREDIENTES":"[('1 Unidade', 'Ovo'), ('3 Colheres', 'A\u00e7ucar'), ('3 Colheres', 'Trigo'), ('3 Colheres', 'Achocolatado'), ('1/4 Colher De Caf\u00e9', 'Fermento'), ('2 Colheres', 'Leite'), ('1/2 Colher De Caf\u00e9', '\u00d3leo De Soja')]",
  "DATA_CRIACAO":"2022-05-20 16:04:14"}])

cursor.execute('select * from receitas')
print('___RECEITAS___')
for receita in cursor.fetchall():
    print(receita[1])

# Adicionando Usuarios
cursor.executemany(
    'INSERT INTO usuarios (APELIDO, NOME, SENHA, EMAIL) VALUES (%s, %s, %s, %s)',
    [
        ('ADMIN0', 'ADMINISTRADOR', 'loveflask', 'email@email.com'),
        ('tsukashi', 'jhony', 'loveflask', 'email@email.com'),
        ('virva', 'bulma', 'esfera', 'email@email.com'),
        ('goku', 'sangaku', '4estrelas', 'email@email.com')
    ]
)

print('___USUARIOS___')
for usuario in cursor.fetchall():
    print(usuario[1])

# commitando senão nada tem efeito
conn.commit()
cursor.close()