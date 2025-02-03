import sqlite3  # Ou o módulo do seu banco de dados
from flask import Flask, g

app = Flask(__name__)
DATABASE = 'bd_norte.db'  # Nome do arquivo do banco de dados

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()