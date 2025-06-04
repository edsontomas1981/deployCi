
class CidadesAtendidas:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = self.conn.cursor()

    def create(self, cidade, filial_responsavel):
        sql = "INSERT INTO cidades_atendidas (cidade, filial_responsavel) VALUES (?, ?)"
        self.cursor.execute(sql, (cidade, filial_responsavel))
        self.conn.commit()
        return self.cursor.lastrowid

    def read(self, id=None):
        if id:
            sql = "SELECT * FROM cidades_atendidas WHERE id = ?"
            self.cursor.execute(sql, (id,))
            return self.cursor.fetchone()
        else:
            sql = "SELECT * FROM cidades_atendidas"
            self.cursor.execute(sql)
            return self.cursor.fetchall()

    def update(self, id, cidade=None, filial_responsavel=None):
        update_fields = []
        values = []
        
        if cidade:
            update_fields.append("cidade = ?")
            values.append(cidade)
        if filial_responsavel:
            update_fields.append("filial_responsavel = ?")
            values.append(filial_responsavel)
            
        if update_fields:
            values.append(id)
            sql = f"UPDATE cidades_atendidas SET {', '.join(update_fields)} WHERE id = ?"
            self.cursor.execute(sql, tuple(values))
            self.conn.commit()
            return True
        return False

    def delete(self, id):
        sql = "DELETE FROM cidades_atendidas WHERE id = ?"
        self.cursor.execute(sql, (id,))
        self.conn.commit()
        return True
    