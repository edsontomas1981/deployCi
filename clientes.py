from conexao import get_db,close_connection

def create_cliente(cliente):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cliente)
    db.commit()

def get_clientes():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM clientes")
    return cursor.fetchall()

def get_cliente_by_cnpj(cnpj):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM clientes WHERE cnpj = ?", (cnpj,))
    return cursor.fetchone()

def update_cliente(cnpj, cliente):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE clientes SET razao = ?, fantasia = ?, cep = ?, logradouro = ?, 
        numero = ?, complemento = ?, bairro = ?, cidade = ?, uf = ?
        WHERE cnpj = ?
    """, cliente + (cnpj,))
    db.commit()

def delete_cliente(cnpj):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM clientes WHERE cnpj = ?", (cnpj,))
    db.commit()