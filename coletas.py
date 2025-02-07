from conexao import get_db,close_connection
from utils import documento_e_valido,busca_cnpj_ws,remove_caracteres_cnpj_cpf
from clientes import get_cliente_by_cnpj,create_cliente

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


def carrega_dados_coleta(json_coletas,msg):
    if (json_coletas['remetente']['cnpj']==''):
        if not documento_e_valido(msg):
            json_coletas['pergunta'] = "Ops! Parece que o documento informado é inválido. Por favor, verifique os dados e tente novamente."            
            return json_coletas

        cnpj_formatado = remove_caracteres_cnpj_cpf(msg)

        cliente = get_cliente_by_cnpj(cnpj_formatado)

        if len(cnpj_formatado) == 14:
            if not cliente:
                response, json_cliente = busca_cnpj_ws(cnpj_formatado)
                if response != 200 or json_cliente.get('status') == 'ERROR' :
                    json_coletas['pergunta'] = "Ops! Parece que algo deu errado. Por favor, verifique os dados e tente novamente."
                    return json_coletas
                
                dados_cliente = []
                dados_cliente.append(cnpj_formatado)    
                dados_cliente.append(json_cliente.get('nome'))
                dados_cliente.append(json_cliente.get('fantasia'))
                dados_cliente.append(json_cliente.get('cep'))
                dados_cliente.append(json_cliente.get('logradouro'))
                dados_cliente.append(json_cliente.get('numero'))
                dados_cliente.append(json_cliente.get('complemento'))
                dados_cliente.append(json_cliente.get('bairro'))   
                dados_cliente.append(json_cliente.get('municipio'))
                dados_cliente.append(json_cliente.get('uf'))
                create_cliente(dados_cliente)
                json_coletas['pergunta'] = "Ops! Parece que o documento informado é inválido. Por favor, verifique os dados e tente novamente."
                return json_coletas
            
            cliente = get_cliente_by_cnpj(cnpj_formatado)

            
            json_coletas['remetente']['cnpj'] = cliente[0]
            json_coletas['remetente']['razao'] = cliente[1]            

            json_coletas['pergunta'] = f"Qual o CNPJ do destinatário?"
            return json_coletas
        
        return json_coletas
    
    if (json_coletas['remetente']['razao']==''):
        json_coletas['remetente']['razao'] = msg
        json_coletas['pergunta'] = f"informe o CEP do remetente"
        return json_coletas
    
    if (json_coletas['destinatario']['cnpj']==''):
        cnpj = processa_cnpj(json_coletas,msg)
        if not cnpj:
            json_coletas['pergunta']="Ops! Parece que algo deu errado. Por favor, verifique os dados e tente novamente."
            return json_coletas

        json_coletas['destinatario']['cnpj']= cnpj
        json_coletas['pergunta'] = "Informe a razão social do destinatario"  #perguntya aqui é a razao social

        razao = processa_razao_social(json_coletas, cnpj) #testa se ele consegue a razao social via sistema
        if razao:
            json_coletas['destinatario']['cnpj']= cnpj
            json_coletas['pergunta']="Informe o cep da coleta"
            return json_coletas

        else:
            json_coletas['destinatario']['razao'] = msg
            json_coletas['pergunta']="Informe o cep da coleta"
            return json_coletas
        



        
        if not cnpj:
            json_coletas['perunta']="Ops! Parece que algo deu errado. Por favor, verifique os dados e tente novamente."

        
        json_coletas['destinatario']['cnpj']  = cnpj
        json_coletas['destinatario']['razao']  = razao

    return json_coletas
    


# def carrega_dados_coleta(json_coletas, msg):
#     """
#     Processa os dados de coleta verificando e buscando informações do remetente.
    
#     Args:
#         json_coletas (dict): Estrutura de dados contendo informações da coleta.
#         msg (str): Mensagem contendo o CNPJ ou outros dados do remetente.
    
#     Returns:
#         dict: Estrutura atualizada de json_coletas.
#     """
#     remetente = json_coletas.get('remetente', {})
    
#     if not remetente.get('cnpj'):
#         return processa_cnpj(json_coletas, msg)
    
#     if not remetente.get('razao'):
#         return processa_razao_social(json_coletas, msg)
    
#     return json_coletas


def processa_cnpj(json_coletas, msg,campo):
    """
    Processa o CNPJ do remetente, validando e buscando informações se necessário.
    
    Args:
        json_coletas (dict): Estrutura de dados contendo informações da coleta.
        msg (str): CNPJ informado.
    
    Returns:
        dict: Estrutura atualizada de json_coletas.
    """

    if not documento_e_valido(msg):
        json_coletas, "Ops! Parece que o documento informado é inválido. Por favor, verifique os dados e tente novamente."
        return  json_coletas,None
    
    cnpj_formatado = remove_caracteres_cnpj_cpf(msg)
    cliente = get_cliente_by_cnpj(cnpj_formatado)
    
    if len(cnpj_formatado) == 14:
        if not cliente:
            cliente_dados = busca_dados_cnpj(cnpj_formatado)
            if not cliente_dados:
                return None
            
            cadastra_cliente(cliente_dados)
            cliente = get_cliente_by_cnpj(cnpj_formatado)

    
    return cliente


def processa_razao_social(json_coletas, msg):
    """
    Define a razão social do remetente.
    
    Args:
        json_coletas (dict): Estrutura de dados contendo informações da coleta.
        msg (str): Razão social informada.
    
    Returns:
        dict: Estrutura atualizada de json_coletas.
    """
    json_coletas['remetente']['razao'] = msg
    return set_pergunta(json_coletas, "Informe o CEP do remetente")


def busca_dados_cnpj(cnpj_formatado):
    """
    Busca informações do CNPJ via web service.
    
    Args:
        cnpj_formatado (str): CNPJ formatado para busca.
    
    Returns:
        list | None: Dados do cliente se encontrado, senão None.
    """
    response, json_cliente = busca_cnpj_ws(cnpj_formatado)
    if response != 200 or json_cliente.get('status') == 'ERROR':
        return None
    
    return [
        cnpj_formatado,
        json_cliente.get('nome'),
        json_cliente.get('fantasia'),
        json_cliente.get('cep'),
        json_cliente.get('logradouro'),
        json_cliente.get('numero'),
        json_cliente.get('complemento'),
        json_cliente.get('bairro'),
        json_cliente.get('municipio'),
        json_cliente.get('uf')
    ]


def cadastra_cliente(dados_cliente):
    """
    Cadastra um novo cliente no banco de dados.
    
    Args:
        dados_cliente (list): Dados do cliente a serem cadastrados.
    """
    create_cliente(dados_cliente)


def set_pergunta(json_coletas, mensagem):
    """
    Define a mensagem de pergunta no json_coletas.
    
    Args:
        json_coletas (dict): Estrutura de dados contendo informações da coleta.
        mensagem (str): Mensagem a ser definida.
    
    Returns:
        dict: Estrutura atualizada de json_coletas.
    """
    json_coletas['pergunta'] = mensagem
    return json_coletas
