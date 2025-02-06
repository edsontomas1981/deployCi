from conexao import get_db,close_connection

def create_contato(contato):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO contato (fone) VALUES (?)", (contato,))
    db.commit()

def get_contatos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contato")
    return cursor.fetchall()

def get_contato_by_id(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contato WHERE id = ?", (id,))
    return cursor.fetchone()

def get_contato_by_fone(fone):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contato WHERE fone = ?", (fone,))
    return cursor.fetchone()

def update_contato(id, contato):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE contato SET fone = ?, clientes_fk = ?
        WHERE id = ?
    """, contato + (id,))
    db.commit()

def update_contato_nome(fone, nome):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(""" UPDATE contato SET nome = ? WHERE fone = ? """, (nome, fone) )
    db.commit()

def delete_contato(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM contato WHERE id = ?", (id,))
    db.commit()