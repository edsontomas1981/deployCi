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

    cnpj_formatado = remove_caracteres_cnpj_cpf(msg)

    def _cria_clientes(json_cliente):

        cliente = get_cliente_by_cnpj(cnpj_formatado)
        if not cliente: 
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

    def _carrega_clientes(cliente,entidade,pergunta):
        cliente = get_cliente_by_cnpj(cnpj_formatado)
        if cliente:
            json_coletas[entidade]['cnpj'] = cliente[0]
            json_coletas[entidade]['razao'] = cliente[1]
            json_coletas[entidade]['cep'] = cliente[3]
            json_coletas[entidade]['rua'] = cliente[4]
            json_coletas[entidade]['numero'] = cliente[5]
            json_coletas[entidade]['complemento'] = cliente[6]
            json_coletas[entidade]['bairro'] = cliente[7]
            json_coletas[entidade]['cidade'] = cliente[8]
            json_coletas[entidade]['uf'] = cliente[9]
            json_coletas['pergunta'] = pergunta
            return json_coletas

    def processar_entidade(json_coletas, msg, entidade,pergunta):
        """
        Processa os dados de uma entidade (remetente, tomador, destinatário) e atualiza json_coletas com a próxima pergunta.
        """
        campos = [
            ('cnpj', "Beleza! Agora me diz o nome do {}."),
            ('razao', "Agora me passa o CEP do {}."),
            ('cep', "E a rua, qual é?"),
            ('rua', "Agora me fala o número do endereço."),
            ('numero', "Tem algum complemento? Se não tiver, só digita 'não'."),
            ('complemento', "E o bairro, qual é?"),
            ('bairro', "Agora me diz a cidade."),
            ('cidade', "E qual é o estado?"),
            ('uf', pergunta)
        ]
        
        for campo, pergunta in campos:
            if json_coletas[entidade][campo] == '':
                json_coletas[entidade][campo] = msg.lower() if campo == 'complemento' else msg
                json_coletas['pergunta'] = pergunta.format(entidade)
                return json_coletas
        
        return json_coletas

    def processar_cnpj(json_coletas, msg, entidade,pergunta):
        """
        Verifica e cadastra o CNPJ da entidade.
        """
        cnpj_formatado = remove_caracteres_cnpj_cpf(msg)
        
        if json_coletas[entidade]['cnpj'] == '' and not documento_e_valido(msg):
            json_coletas['pergunta'] = "Ops! Parece que o documento informado é inválido. Por favor, verifique os dados e tente novamente."
            return json_coletas
        
        cliente = get_cliente_by_cnpj(cnpj_formatado)

        if cliente:
            _carrega_clientes(cliente,entidade,"Agora me passa o CNPJ do destinatário.")
            return json_coletas

        if len(cnpj_formatado) == 14 and not cliente:
            response, json_cliente = busca_cnpj_ws(cnpj_formatado)
            if response != 200 or json_cliente.get('status') == 'ERROR':
                json_coletas['pergunta'] = "Ops! Parece que algo deu errado. Por favor, verifique os dados e tente novamente."
                return json_coletas
            # Se conseguiu buscar os dados

            _cria_clientes(json_cliente)
            return json_coletas

        
        return processar_entidade(json_coletas, msg, entidade,pergunta)

    def processar_dados(json_coletas, msg, campos_vazios, entidade,pergunta_final):
        """
        Processa os dados e retorna json_coletas atualizado.
        """
        if len(campos_vazios) > 0:
            return processar_cnpj(json_coletas, msg, entidade,pergunta_final)
        
        return json_coletas
    
    cnpj_formatado = remove_caracteres_cnpj_cpf(msg)

    campos_vazios = [campo for campo, valor in json_coletas['remetente'].items() if valor == '']

    if len(campos_vazios)>0:
        processar_dados(json_coletas,msg,campos_vazios,'remetente',"Agora me passa o CNPJ do destinatário.")
        return json_coletas
    

    campos_vazios = [campo for campo, valor in json_coletas['destinatario'].items() if valor == '']

    if len(campos_vazios)>0:
        processar_dados(json_coletas,msg,campos_vazios,'destinatario',"Quantos volumes serão retirados.")
        return json_coletas

    # print(f" json coletas{json_coletas}")
    # json_coletas['pergunta'] = 'teste'
    # return(json_coletas)


    # processar_dados(json_coletas,msg,campos_vazios)

    '''
    # campos_vazios = [campo for campo, valor in json_coletas['remetente'].items() if valor == '']

    
    # if len(campos_vazios)>0:
    #     cnpj_formatado = remove_caracteres_cnpj_cpf(msg)

    #     if json_coletas['remetente']['cnpj']=='':
    #         if not documento_e_valido(msg):
    #             json_coletas['pergunta'] = "Ops! Parece que o documento informado é inválido. Por favor, verifique os dados e tente novamente."            
    #             return json_coletas

    #     cliente = get_cliente_by_cnpj(cnpj_formatado)

    #     # json_coletas = _carrega_clientes(cliente,'remetente',"Agora me passa o CNPJ do destinatário.")

    #     # if len(cnpj_formatado) == 14: #Se for um Cnpj Busca e cadastra.
    #     #     if not cliente:
    #     #         response, json_cliente = busca_cnpj_ws(cnpj_formatado)
    #     #         if response != 200 or json_cliente.get('status') == 'ERROR' :
    #     #             json_coletas['pergunta'] = "Ops! Parece que algo deu errado. Por favor, verifique os dados e tente novamente."
    #     #             return json_coletas
    #     #         _cria_clientes(json_cliente)
            
    #     #     if json_coletas['remetente']['cnpj'] == '':
    #     #         json_coletas['remetente']['cnpj'] = msg
    #     #         json_coletas['pergunta'] = "Beleza! Agora me diz o nome do cliente."
    #     #         return json_coletas

    #     #     cliente = get_cliente_by_cnpj(cnpj_formatado)

    #     #     _carrega_clientes(cliente,'remetente',"Agora me passa o CNPJ do destinatário.")

    #     #     if json_coletas['remetente']['razao'] == '':
    #     #         json_coletas['remetente']['razao'] = msg
    #     #         json_coletas['pergunta'] = "Agora me passa o CEP do cliente."
    #     #         return json_coletas

    #     #     if json_coletas['remetente']['cep'] == '':
    #     #         json_coletas['remetente']['cep'] = msg
    #     #         json_coletas['pergunta'] = "E a rua, qual é?"
    #     #         return json_coletas  

    #     #     if json_coletas['remetente']['rua'] == '':
    #     #         json_coletas['remetente']['rua'] = msg
    #     #         json_coletas['pergunta'] = "Agora me fala o número do endereço."
    #     #         return json_coletas           

    #     #     if json_coletas['remetente']['numero'] == '':
    #     #         json_coletas['remetente']['numero'] = msg
    #     #         json_coletas['pergunta'] = "Tem algum complemento? Se não tiver, só digita 'não'."
    #     #         return json_coletas    

    #     #     if json_coletas['remetente']['complemento'] == '':
    #     #         msg = msg.lower()
    #     #         if msg in ['não', 'nao']:
    #     #             msg = ''
    #     #         json_coletas['remetente']['complemento'] = msg
    #     #         json_coletas['pergunta'] = "E o bairro, qual é?"
    #     #         return json_coletas                       

    #     #     if json_coletas['remetente']['bairro'] == '':
    #     #         json_coletas['remetente']['bairro'] = msg
    #     #         json_coletas['pergunta'] = "Agora me diz a cidade."
    #     #         return json_coletas     

    #     #     if json_coletas['remetente']['cidade'] == '':
    #     #         json_coletas['remetente']['cidade'] = msg
    #     #         json_coletas['pergunta'] = "E qual é o estado?"
    #     #         return json_coletas                                            

    #     #     if json_coletas['remetente']['uf'] == '':
    #     #         json_coletas['remetente']['uf'] = msg
    #     #         json_coletas['pergunta'] = "Agora me passa o CNPJ do destinatário."
    #     #         return json_coletas
            
    #     #     return json_coletas

    #     # else:
    #     #     if json_coletas['remetente']['cnpj'] == '':
    #     #         json_coletas['remetente']['cnpj'] = msg
    #     #         json_coletas['pergunta'] = "Beleza! Agora me diz o nome do remetente."
    #     #         return json_coletas

    #     #     if json_coletas['remetente']['razao'] == '':
    #     #         json_coletas['remetente']['razao'] = msg
    #     #         json_coletas['pergunta'] = "Agora me passa o CEP do remetente."
    #     #         return json_coletas

    #     #     if json_coletas['remetente']['cep'] == '':
    #     #         json_coletas['remetente']['cep'] = msg
    #     #         json_coletas['pergunta'] = "E a rua, qual é?"
    #     #         return json_coletas  

    #     #     if json_coletas['remetente']['rua'] == '':
    #     #         json_coletas['remetente']['rua'] = msg
    #     #         json_coletas['pergunta'] = "Agora me fala o número do endereço."
    #     #         return json_coletas           

    #     #     if json_coletas['remetente']['numero'] == '':
    #     #         json_coletas['remetente']['numero'] = msg
    #     #         json_coletas['pergunta'] = "Tem algum complemento? Se não tiver, só digita 'não'."
    #     #         return json_coletas    

    #     #     if json_coletas['remetente']['complemento'] == '':
    #     #         msg = msg.lower()
    #     #         json_coletas['remetente']['complemento'] = msg
    #     #         json_coletas['pergunta'] = "E o bairro, qual é?"
    #     #         return json_coletas                       

    #     #     if json_coletas['remetente']['bairro'] == '':
    #     #         json_coletas['remetente']['bairro'] = msg
    #     #         json_coletas['pergunta'] = "Agora me diz a cidade."
    #     #         return json_coletas     

    #     #     if json_coletas['remetente']['cidade'] == '':
    #     #         json_coletas['remetente']['cidade'] = msg
    #     #         json_coletas['pergunta'] = "E qual é o estado?"
    #     #         return json_coletas                                            

    #     #     if json_coletas['remetente']['uf'] == '':
    #     #         json_coletas['remetente']['uf'] = msg
    #     #         json_coletas['pergunta'] = "Agora me passa o CNPJ do destinatário."
    #     #         return json_coletas
            
    #     #     return json_coletas

    # campos_vazios = [campo for campo, valor in json_coletas['destinatario'].items() if valor == '']

    # print(campos_vazios)
    
    # if len(campos_vazios)>0:
    #     cnpj_formatado = remove_caracteres_cnpj_cpf(msg)

    #     if json_coletas['destinatario']['cnpj']=='':
    #         if not documento_e_valido(msg):
    #             json_coletas['pergunta'] = "Ops! Parece que o documento informado é inválido. Por favor, verifique os dados e tente novamente."            
    #             return json_coletas

    #     cliente = get_cliente_by_cnpj(cnpj_formatado)

    #     json_coletas = _carrega_clientes(cliente,'destinatario',"Agora me passa o CNPJ do destinatário.")

    #     if len(cnpj_formatado) == 14: #Se for um Cnpj Busca e cadastra.
    #         if not cliente:
    #             response, json_cliente = busca_cnpj_ws(cnpj_formatado)
    #             if response != 200 or json_cliente.get('status') == 'ERROR' :
    #                 json_coletas['pergunta'] = "Ops! Parece que algo deu errado. Por favor, verifique os dados e tente novamente."
    #                 return json_coletas
    #             _cria_clientes(json_cliente)
            
    #         if json_coletas['destinatario']['cnpj'] == '':
    #             json_coletas['destinatario']['cnpj'] = msg
    #             json_coletas['pergunta'] = "Beleza! Agora me diz o nome do cliente."
    #             return json_coletas

    #         cliente = get_cliente_by_cnpj(cnpj_formatado)

    #         _carrega_clientes(cliente,'destinatario',"Agora me passa os volumes.")

    #         if json_coletas['destinatario']['razao'] == '':
    #             json_coletas['destinatario']['razao'] = msg
    #             json_coletas['pergunta'] = "Agora me passa o CEP do cliente."
    #             return json_coletas

    #         if json_coletas['destinatario']['cep'] == '':
    #             json_coletas['destinatario']['cep'] = msg
    #             json_coletas['pergunta'] = "E a rua, qual é?"
    #             return json_coletas  

    #         if json_coletas['destinatario']['rua'] == '':
    #             json_coletas['destinatario']['rua'] = msg
    #             json_coletas['pergunta'] = "Agora me fala o número do endereço."
    #             return json_coletas           

    #         if json_coletas['destinatario']['numero'] == '':
    #             json_coletas['destinatario']['numero'] = msg
    #             json_coletas['pergunta'] = "Tem algum complemento? Se não tiver, só digita 'não'."
    #             return json_coletas    

    #         if json_coletas['destinatario']['complemento'] == '':
    #             print('pq entrou aqui cnpj')
    #             msg = msg.lower()
    #             if msg in ['não', 'nao']:
    #                 msg = ''
    #             json_coletas['destinatario']['complemento'] = msg
    #             json_coletas['pergunta'] = "E o bairro, qual é?"
    #             return json_coletas                       

    #         if json_coletas['destinatario']['bairro'] == '':
    #             json_coletas['destinatario']['bairro'] = msg
    #             json_coletas['pergunta'] = "Agora me diz a cidade."
    #             return json_coletas     

    #         if json_coletas['destinatario']['cidade'] == '':
    #             json_coletas['destinatario']['cidade'] = msg
    #             json_coletas['pergunta'] = "E qual é o estado?"
    #             return json_coletas                                            

    #         if json_coletas['destinatario']['uf'] == '':
    #             json_coletas['destinatario']['uf'] = msg
    #             json_coletas['pergunta'] = "Agora me passa quantos volumes."
    #             return json_coletas
            
    #         return json_coletas

    #     else:
    #         if json_coletas['destinatario']['cnpj'] == '':
    #             json_coletas['destinatario']['cnpj'] = msg
    #             json_coletas['pergunta'] = "Beleza! Agora me diz o nome do destinatário."
    #             return json_coletas

    #         if json_coletas['destinatario']['razao'] == '':
    #             json_coletas['destinatario']['razao'] = msg
    #             json_coletas['pergunta'] = "Agora me passa o CEP do destinatário."
    #             return json_coletas

    #         if json_coletas['destinatario']['cep'] == '':
    #             json_coletas['destinatario']['cep'] = msg
    #             json_coletas['pergunta'] = "E a rua, qual é?"
    #             return json_coletas  

    #         if json_coletas['destinatario']['rua'] == '':
    #             json_coletas['destinatario']['rua'] = msg
    #             json_coletas['pergunta'] = "Agora me fala o número do endereço."
    #             return json_coletas           

    #         if json_coletas['destinatario']['numero'] == '':
    #             json_coletas['destinatario']['numero'] = msg
    #             json_coletas['pergunta'] = "Tem algum complemento? Se não tiver, só digita 'não'."
    #             return json_coletas    

    #         if json_coletas['destinatario']['complemento'] == '':
    #             print('pq entrou aqui cpf')
    #             msg = msg.lower()
    #             if msg in ['não', 'nao']:
    #                 msg = ''
    #             json_coletas['destinatario']['complemento'] = msg
    #             json_coletas['pergunta'] = "E o bairro, qual é?"
    #             return json_coletas                       

    #         if json_coletas['destinatario']['bairro'] == '':
    #             json_coletas['destinatario']['bairro'] = msg
    #             json_coletas['pergunta'] = "Agora me diz a cidade."
    #             return json_coletas     

    #         if json_coletas['destinatario']['cidade'] == '':
    #             json_coletas['destinatario']['cidade'] = msg
    #             json_coletas['pergunta'] = "E qual é o estado?"
    #             return json_coletas                                            

    #         if json_coletas['destinatario']['uf'] == '':
    #             json_coletas['destinatario']['uf'] = msg
    #             json_coletas['pergunta'] = "Agora me passa quantos volumes."
    #             return json_coletas
            
    #         return json_coletas
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

'''