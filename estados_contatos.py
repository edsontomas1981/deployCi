from conexao import get_db,close_connection

def create_estado_contato(estado_contato):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO estados_contatos (telefone, estado_atual, dados,passo) 
        VALUES (?, ?, ?,?)
    """, estado_contato)
    db.commit()

def get_estados_contatos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM estados_contatos")
    return cursor.fetchall()

def get_estado_contato_by_telefone(telefone):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM estados_contatos WHERE telefone = ?", (telefone,))    
    return cursor.fetchone()

def update_estado_contato(telefone, novo_estado, novo_passo, dados):
    print(telefone, novo_estado, novo_passo, dados)
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("""
        UPDATE estados_contatos
        SET estado_atual = ?, dados = ?, passo = ?
        WHERE telefone = ?
    """, (novo_estado, dados, novo_passo, telefone))
    
    db.commit()

def delete_estado_contato(telefone):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM estados_contatos WHERE telefone = ?", (telefone,))
    db.commit()