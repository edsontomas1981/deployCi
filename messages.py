from conexao import get_db,close_connection

# Funções para executar as queries SQL para a tabela mensagens
def create_mensagem(mensagem):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO mensagens (contato_fk, msg) VALUES (?, ?)", mensagem)  # Data é automática
    db.commit()

def get_mensagens():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mensagens")
    return cursor.fetchall()

def get_mensagem_by_id(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mensagens WHERE id = ?", (id,))
    return cursor.fetchone()

def update_mensagem(id, mensagem):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE mensagens SET contato_fk = ?, msg = ?
        WHERE id = ?
    """, mensagem + (id,))
    db.commit()

def delete_mensagem(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM mensagens WHERE id = ?", (id,))
    db.commit()
