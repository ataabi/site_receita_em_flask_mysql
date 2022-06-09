import os

SECRET_KEY = 'ChaveSuperSecreta'
# app.run(host='192.168.10.5', port=5000)
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "root1"
MYSQL_DB = "site_receitas"
MYSQL_PORT = 3306
UPLOADS_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
