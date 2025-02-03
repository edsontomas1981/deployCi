from conexao import get_db,close_connection

def create_coleta(coleta):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO coleta (remetente_fk, destinatario_fk, volumes, peso, num_nf, 
                           tipo_mercadoria, nome, metragem_cubica, horario, fone, 
                           cep, logradouro, numero, complemento, cidade, uf, lat, lng) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, coleta)
    db.commit()

def get_coletas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM coleta")
    return cursor.fetchall()

def get_coleta_by_id(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM coleta WHERE id = ?", (id,))
    return cursor.fetchone()

def update_coleta(id, coleta):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE coleta SET remetente_fk = ?, destinatario_fk = ?, volumes = ?, 
                         peso = ?, num_nf = ?, tipo_mercadoria = ?, nome = ?, 
                         metragem_cubica = ?, horario = ?, fone = ?, cep = ?, 
                         logradouro = ?, numero = ?, complemento = ?, cidade = ?, 
                         uf = ?, lat = ?, lng = ?
        WHERE id = ?
    """, coleta + (id,))
    db.commit()

def delete_coleta(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM coleta WHERE id = ?", (id,))
    db.commit()