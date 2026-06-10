from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = "super_secret_bookstore_key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'livraria_bd'

mysql = MySQL(app)