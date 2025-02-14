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


def _processa_carga(json_coletas,entidade,msg,campos):
    # campos = [
    #     ('volumes', "Qual é a metragem desses volumes? Pode ser só da maior, tipo 1,0 x 0,59 x 0,89."),
    #     ('m3', "Agora, qual é o peso total dessa carga?"),
    #     ('peso', "Qual é o valor desses produtos?"),
    #     ('valor_nf', "E o número da nota fiscal, você já tem? Se ainda não tiver, é só digitar 'não'."),
    #     ('num_nf', "Legal! Agora, confirma os dados: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Está tudo certo ou deseja alterar alguma informação? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."),
    #     # ('num_nf', "Legal! Agora vamos conferir o endereço da coleta. Me informa qual é o CEP?"),
    # ]

    for campo, pergunta in campos:
        if json_coletas[entidade][campo] == '':
            json_coletas[entidade][campo] = msg.lower()
            json_coletas['pergunta'] = pergunta.format(json_coletas[entidade].get('volumes'),json_coletas[entidade].get('peso'),
                                                        json_coletas[entidade].get('m3'),json_coletas[entidade].get('valor_nf')
                                                        ,json_coletas[entidade].get('num_nf'))
            return json_coletas
    return json_coletas


def carrega_dados_coleta(json_coletas,msg):

    cnpj_formatado = remove_caracteres_cnpj_cpf(msg)

    def _processa_dados_da_carga(json_coletas,entidade):
        if not json_coletas[entidade]['confirmacao']:
            campos = [
                ('volumes', "Qual é a metragem desses volumes? Pode ser só da maior, tipo 1,0 x 0,59 x 0,89."),
                ('m3', "Agora, qual é o peso total dessa carga?"),
                ('peso', "Qual é o valor desses produtos?"),
                ('valor_nf', "E o número da nota fiscal, você já tem? Se ainda não tiver, é só digitar 'não'."),
                ('num_nf', "Ótimo! Agora, confirme os dados: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Está tudo correto ou deseja fazer alguma alteração? Digite 'alterar' para modificar os dados ou 'confirmar' para prosseguir."),
            ]

        else:
            campos = [
                ('volumes', "Ótimo! Agora, só para confirmar: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Tudo certo ou quer modificar alguma informação? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."),
                ('m3', "Ótimo! Agora, só para confirmar: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Tudo certo ou quer modificar alguma informação? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."),
                ('peso', "Ótimo! Agora, só para confirmar: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Tudo certo ou quer modificar alguma informação? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."),
                ('valor_nf', "Ótimo! Agora, só para confirmar: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Tudo certo ou quer modificar alguma informação? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."),
                ('num_nf', "Ótimo! Agora, só para confirmar: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Tudo certo ou quer modificar alguma informação? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."),
                # ('num_nf', "Legal! Agora vamos conferir o endereço da coleta. Me informa qual é o CEP?"),
            ]


        for campo, pergunta in campos:
            if json_coletas[entidade][campo] == '':
                json_coletas[entidade][campo] = msg.lower()
                json_coletas['pergunta'] = pergunta.format(json_coletas[entidade].get('volumes'),json_coletas[entidade].get('peso'),
                                                           json_coletas[entidade].get('m3'),json_coletas[entidade].get('valor_nf')
                                                           ,json_coletas[entidade].get('num_nf'))
                json_coletas[entidade]['confirmacao'] = False
                json_coletas[entidade]['estado_finalizacao'] = 'aguardando'
                return json_coletas
            
        json_coletas[entidade]['confirmacao'] = False
        json_coletas[entidade]['estado_finalizacao'] = 'aguardando'
        return json_coletas

    def _cria_clientes(json_cliente):
        print('esta cirando o cliente no bd')
        cnpj_formatado = remove_caracteres_cnpj_cpf(json_cliente.get('cnpj'))
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

    def _carrega_clientes(cliente, entidade, pergunta, json_coletas):
        """
        Preenche os dados do cliente no dicionário json_coletas.
        """
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
        return json_coletas  # Retorna o objeto atualizado

    def processar_entidade(json_coletas, msg, entidade,pergunta):
        """
        Processa os dados de uma entidade (remetente, tomador, destinatário) e atualiza json_coletas com a próxima pergunta.
        """
        def _prepara_campos(cliente_json):
            return {
                    "bairro":cliente_json.get("bairro"),
                    "cep":cliente_json.get("cep"),
                    "municipio":cliente_json.get("cidade"),
                    "cnpj":cliente_json.get("cnpj"),
                    "complemento":cliente_json.get("complemento","Não Informado"),
                    "numero":cliente_json.get("numero"),
                    "nome":cliente_json.get("razao"),
                    "fantasia":cliente_json.get("razao"),
                    "logradouro":cliente_json.get("rua"),
                    "uf":cliente_json.get("uf"),
                }
        
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
                if campo == 'complemento':
                    if json_coletas[entidade][campo] == '':
                        json_coletas[entidade][campo] == 'Não Informado'

                json_coletas['pergunta'] = pergunta.format(entidade)
                if campo == 'uf':
                    _cria_clientes(_prepara_campos(json_coletas[entidade]))
                return json_coletas

        return json_coletas

    def processar_cnpj(json_coletas, msg, entidade, pergunta):
        """
        Verifica e cadastra o CNPJ da entidade.
        """
        cnpj_formatado = remove_caracteres_cnpj_cpf(msg)
        
        if json_coletas[entidade]['cnpj'] == '' and not documento_e_valido(msg):
            json_coletas['pergunta'] = "Ops! Parece que o documento informado é inválido. Por favor, verifique os dados e tente novamente."
            return json_coletas
        
        cliente = get_cliente_by_cnpj(cnpj_formatado)

        if cliente:
            return _carrega_clientes(cliente, entidade, pergunta, json_coletas)  # Passa json_coletas corretamente

        if len(cnpj_formatado) == 14:
            response, json_cliente = busca_cnpj_ws(cnpj_formatado)
            if response != 200 or json_cliente.get('status') == 'ERROR':
                json_coletas['pergunta'] = "Ops! Parece que algo deu errado. Por favor, verifique os dados e tente novamente."
                return json_coletas
            _cria_clientes(json_cliente)
            # Buscar novamente o cliente cadastrado
            cliente = get_cliente_by_cnpj(cnpj_formatado)

            if cliente:
                return _carrega_clientes(cliente, entidade, pergunta, json_coletas)  # Passa json_coletas corretamente

        return processar_entidade(json_coletas, msg, entidade, pergunta)

    def processar_dados(json_coletas, msg, campos_vazios, entidade,pergunta_final):
        """
        Processa os dados e retorna json_coletas atualizado.
        """
        if len(campos_vazios) > 0:
            return processar_cnpj(json_coletas, msg, entidade,pergunta_final)
        
        return json_coletas
    
    campos_vazios = [campo for campo, valor in json_coletas['remetente'].items() if valor == '']
    if len(campos_vazios)>0:
        processar_dados(json_coletas,msg,campos_vazios,'remetente',"Agora me passa o CNPJ do destinatário.")
        return json_coletas
    
    campos_vazios = [campo for campo, valor in json_coletas['destinatario'].items() if valor == '']
    if len(campos_vazios)>0:
        processar_dados(json_coletas,msg,campos_vazios,'destinatario',"Quantos volumes vão ser retirados?")
        return json_coletas

    json_coletas['pergunta'] = "Quantos volumes vão ser retirados?"
    campos_vazios = [campo for campo, valor in json_coletas['dados_coleta'].items() if valor == '']
    if len(campos_vazios)>0:
        _processa_dados_da_carga(json_coletas,'dados_coleta')
        return json_coletas


    if json_coletas['dados_coleta']['estado_finalizacao']=='aguardando':

        if msg.lower() == 'confirmar':
            json_coletas['dados_coleta']['estado_finalizacao'] = 'finalizado'
            return json_coletas

        if msg.lower() == 'alterar':
            json_coletas['dados_coleta']['confirmacao'] = True
            json_coletas['dados_coleta']['estado_finalizacao'] = 'editando'
            json_coletas['pergunta'] = "Qual dado você deseja alterar? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."
            # return json_coletas

    if json_coletas['dados_coleta']['estado_finalizacao']=='editando':
        match msg:
            case '1':
                json_coletas['dados_coleta']['volumes'] = ''
                json_coletas['dados_coleta']['confirmacao'] = True
                json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
                return json_coletas
            case '2':
                json_coletas['dados_coleta']['peso'] = ''
                json_coletas['dados_coleta']['confirmacao'] = True
                json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'

                return json_coletas
            case '3':
                print('correcao m3')
                json_coletas['dados_coleta']['m3'] = ''
                json_coletas['dados_coleta']['confirmacao'] = True
                json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
                return json_coletas
            case '4':
                json_coletas['dados_coleta']['valor_nf'] = ''
                json_coletas['dados_coleta']['confirmacao'] = True
                json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
                return json_coletas
            case '5':
                json_coletas['dados_coleta']['num_nf'] = ''
                json_coletas['dados_coleta']['confirmacao'] = True
                json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
                return json_coletas

    return json_coletas    


