from conexao import get_db,close_connection
from utils import documento_e_valido,busca_cnpj_ws,remove_caracteres_cnpj_cpf,validar_cep,imprimirJsonTerminal
from clientes import get_cliente_by_cnpj,create_cliente
from cep import busca_cep

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

    def _processa_proximo_campo(json_coletas,entidade, campos, campo_atual):
        
        for campo in campos:
            if json_coletas[entidade][campo] == '' and campo != campo_atual :
                return campo
        
        return None
    
    def _processa_campo_atual(json_coletas,entidade, campos):
        for campo in campos:
            print(f'Campo: {campo} valor do campo:{json_coletas[entidade][campo]} ')
            if json_coletas[entidade][campo] == '' or not json_coletas[entidade][campo]:
                return campo
        return None
            
    def _processa_dados_da_carga(json_coletas,entidade):
        print(f'Dados Da Carga {json_coletas['pergunta']}')
        if not json_coletas[entidade]['confirmacao']:
            campos = [
                ('volumes', "Qual é a metragem desses volumes? Pode ser só da maior, tipo 1,0 x 0,59 x 0,89."),
                ('m3', "Agora, qual é o peso total dessa carga?"),
                ('peso', "Qual é o valor desses produtos?"),
                ('valor_nf', "E o número da nota fiscal, você já tem? Se ainda não tiver, é só digitar 'não'."),
                ('num_nf', "Ótimo! Agora, confirme os dados: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Está tudo correto ou deseja fazer alguma alteração? Digite 'alterar' para modificar os dados ou 'confirma' para prosseguir."),
            ]

        else:
            campos = [
                ('volumes', "Perfeito! Agora, revise os dados: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Está tudo certo ou precisa ajustar algo? Digite 'alterar' para modificar ou 'confirma' para continuar."),
                ('m3', "Ótimo! Confira os dados informados: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Caso precise corrigir algo, digite 'alterar'. Para seguir, digite 'confirma'."),
                ('peso', "Tudo certo até aqui! Veja os detalhes: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Se precisar mudar algo, digite 'alterar'. Para continuar, digite 'confirma'."),
                ('valor_nf', "Estamos quase lá! Verifique os dados abaixo: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Caso precise editar, digite 'alterar'. Se estiver correto, digite 'confirma'."),
                ('num_nf', "Revise as informações: Volumes: {}, Peso: {} kg, M³: {}, Valor: R$ {}, Nota Fiscal Nº {}. Tudo certo? Digite 'alterar' para corrigir ou 'confirma' para avançar."),
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

    # campos_vazios = [campo for campo, valor in json_coletas['remetente'].items() if valor == '']
    # if len(campos_vazios)>0:
    #     processar_dados(json_coletas,msg,campos_vazios,'remetente',"Agora me passa o CNPJ do destinatário.")
    #     return json_coletas
    
    # campos_vazios = [campo for campo, valor in json_coletas['destinatario'].items() if valor == '']
    # if len(campos_vazios)>0:
    #     processar_dados(json_coletas,msg,campos_vazios,'destinatario',"Quantos volumes vão ser retirados?")
    #     return json_coletas

    # campos_vazios = [campo for campo, valor in json_coletas['dados_coleta'].items() if valor == '']
    # if len(campos_vazios)>0:
    #     _processa_dados_da_carga(json_coletas,'dados_coleta')
    #     return json_coletas

    # if json_coletas['dados_coleta']['estado_finalizacao']=='aguardando':

    #     if msg.lower() == 'confirma':
    #         json_coletas['dados_coleta']['estado_finalizacao'] = 'finalizado'
    #         json_coletas['pergunta'] = "Me passa o CEP da coleta, por favor!"
    #         return json_coletas

    #     if msg.lower() == 'alterar':
            # json_coletas['dados_coleta']['confirmacao'] = True
            # json_coletas['dados_coleta']['estado_finalizacao'] = 'editando'
            # json_coletas['pergunta'] = "Qual dado você deseja alterar? (1) Volumes, (2) Peso, (3) M³, (4) Valor, (5) Nota Fiscal."

    # if json_coletas['dados_coleta']['estado_finalizacao']=='editando':
    #     match msg:
    #         case '1':
    #             json_coletas['dados_coleta']['volumes'] = ''
    #             json_coletas['dados_coleta']['confirmacao'] = True
    #             json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
    #             json_coletas['pergunta'] = "Me diz aí, quantos volumes vão ser retirados?"
    #             return json_coletas
    #         case '2':
    #             json_coletas['dados_coleta']['peso'] = ''
    #             json_coletas['dados_coleta']['confirmacao'] = True
    #             json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
    #             json_coletas['pergunta'] = "Beleza! Agora me diz o peso correto em kg."
    #             return json_coletas
    #         case '3':
    #             json_coletas['dados_coleta']['m3'] = ''
    #             json_coletas['dados_coleta']['confirmacao'] = True
    #             json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
    #             json_coletas['pergunta'] = "Ótimo! Agora me diz as dimensões corretas."
    #             return json_coletas
    #         case '4':
    #             json_coletas['dados_coleta']['valor_nf'] = ''
    #             json_coletas['dados_coleta']['confirmacao'] = True
    #             json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
    #             json_coletas['pergunta'] = "Legal! Agora me diz o valor correto da nota fiscal."
    #             return json_coletas
    #         case '5':
    #             json_coletas['dados_coleta']['num_nf'] = ''
    #             json_coletas['dados_coleta']['confirmacao'] = True
    #             json_coletas['dados_coleta']['estado_finalizacao'] = 'aguardando'
    #             json_coletas['pergunta'] = "Legal! Agora me diz o número correto da nota fiscal."
    #             return json_coletas
    
    def popula_json_coletas(entidade,campos,valor):
        for campo in campos:
            json_coletas[entidade][campo] = valor

    def obter_mensagem_pergunta(campo):
        """Retorna a mensagem correspondente ao campo solicitado."""
        mensagens = {
            'cep': "Me passa o CEP da coleta, por favor!",
            'rua': "E a rua, qual é?",
            'num': "Agora me fala o número do endereço.",
            'complemento': "Tem algum complemento? Se não tiver, só digita 'não'.",
            'bairro': "E o bairro, qual é?",
            'cidade': "Agora me diz a cidade.",
            'uf': "E qual é o estado?",
        }
        return mensagens.get(campo, "Qual informação deseja atualizar?")


    def validar_e_buscar_cep(cep):
        
        """Valida e busca os dados do CEP."""

        if not validar_cep(cep):
            return None

        dados_cep = busca_cep(cep)

        return {
            'cep': dados_cep.get('cep', cep),
            'rua': dados_cep.get('street', ""),
            'bairro': dados_cep.get('neighborhood', ""),
            'cidade': dados_cep.get('city', ""),
            'uf': dados_cep.get('state', ""),
        }


    def atualizar_endereco_coleta(json_coletas, msg):
        """Atualiza os dados de coleta com base na entrada do usuário."""
        endereco = json_coletas['endereco_coleta']
        
        if not endereco['cep']:
            dados_cep = validar_e_buscar_cep(msg)
            if not dados_cep:
                json_coletas['pergunta'] = "Opa! Esse CEP parece inválido. Dá uma conferida e tenta de novo."
                return json_coletas
            
            endereco.update(dados_cep)

        campo_atual = _processa_campo_atual(json_coletas, 'endereco_coleta', list(obter_mensagem_pergunta.keys()))
        if campo_atual:
            endereco[campo_atual] = msg
            proximo_campo = _processa_proximo_campo(json_coletas, 'endereco_coleta', list(obter_mensagem_pergunta.keys()), campo_atual)

            json_coletas['pergunta'] = (
                obter_mensagem_pergunta(proximo_campo) 
                if proximo_campo 
                else confirmar_endereco(json_coletas)
            )
            return json_coletas

        return processar_estado_coleta(json_coletas, msg)


    def confirmar_endereco(json_coletas):
        """Gera a mensagem final de confirmação do endereço de coleta."""
        endereco = json_coletas['endereco_coleta']
        return f"""Ótimo! Agora, confirme o endereço de coleta:
        CEP: {endereco['cep']}, Rua: {endereco['rua']}, Nº: {endereco['num']}, 
        Complemento: {endereco['complemento']}, Bairro: {endereco['bairro']}, 
        Cidade: {endereco['cidade']}, Estado: {endereco['uf']}.
        Está tudo correto ou deseja fazer alguma alteração?
        Digite 'editar' para modificar os dados ou 'ok' para prosseguir."""


    def processar_estado_coleta(json_coletas, msg):
        """Gerencia o estado da coleta e edições."""

        estado = json_coletas['endereco_coleta']['state']
        
        if estado == "aguardando":
            if msg == "editar":
                json_coletas['endereco_coleta']['state'] = "editando"
                json_coletas['pergunta'] = "Qual dado você deseja alterar? (1) CEP, (2) Rua, (3) Número, (4) Complemento, (5) Bairro, (6) Cidade, (7) Estado."
            elif msg == "ok":
                json_coletas['endereco_coleta']['state'] = "finalizado"
                json_coletas['pergunta'] = "Ótimo! Agora me passa o CEP da coleta, por favor!"
        
        elif estado == "editando":
            opcoes = ["cep", "rua", "num", "complemento", "bairro", "cidade", "uf"]
            if msg.isdigit() and 1 <= int(msg) <= 7:
                campo = opcoes[int(msg) - 1]
                json_coletas['endereco_coleta'][campo] = ''
                json_coletas['endereco_coleta']['state'] = "aguardando"
                json_coletas['pergunta'] = obter_mensagem_pergunta(campo)
        elif estado == "editando":
            pass        
        return json_coletas
    
   
    print(processar_estado_coleta(json_coletas,msg))

    # json_coletas['pergunta'] = "Me passa o CEP da coleta, por favor!"

    # dict_verificacao = {'cep': "Me passa o CEP da coleta, por favor!",
    #     'rua': "E a rua, qual é?",
    #     'num':"Agora me fala o número do endereço.",
    #     'complemento':  "Tem algum complemento? Se não tiver, só digita 'não'.",        
    #     'bairro':"E o bairro, qual é?",
    #     'cidade':  "Agora me diz a cidade.",
    #     'uf':"E qual é o estado?",
    #     'dados_coleta': 'dados_coleta',
    #     'pergunta_final':f"""Ótimo! Agora, confirme o endereco de coleta: CEP: {json_coletas['endereco_coleta']['cep']}, 
    #                             Endereço: {json_coletas['endereco_coleta']['rua']},Nº: {json_coletas['endereco_coleta']['num']}, 
    #                             Complemento: {json_coletas['endereco_coleta']['complemento']}, 
    #                             Bairro: {json_coletas['endereco_coleta']['bairro']}, Cidade: {json_coletas['endereco_coleta']['cidade']}, 
    #                             Estado: {json_coletas['endereco_coleta']['uf']}.\n
    #                             Está tudo correto ou deseja fazer alguma alteração? 
    #                             Digite 'editar' para modificar os dados ou 'ok' para prosseguir.""",
    #                             }


    # campos_endereco_entrega = ['cep','rua','num','complemento','bairro','cidade','uf']

    # print(f'State: {json_coletas['endereco_coleta']['state']}')
    
    # if json_coletas['endereco_coleta']['cep'] == '':
        
    #     if not validar_cep(msg):
    #         json_coletas['pergunta'] = 'Opa! Esse CEP parece inválido. Dá uma conferida e tenta de novo.'
    #         return json_coletas
        
    #     cep = busca_cep(msg)

    #     print(f'CEP: {cep}')

    #     json_coletas['endereco_coleta']['cep'] = cep.get('cep') if cep.get('cep') else msg
    #     json_coletas['endereco_coleta']['rua'] = cep.get('street') if cep.get('street') else ""
    #     json_coletas['endereco_coleta']['bairro'] = cep.get('neighborhood') if cep.get('neighborhood') else ""
    #     json_coletas['endereco_coleta']['cidade'] = cep.get('city',"") if cep.get('city') else ""
    #     json_coletas['endereco_coleta']['uf'] = cep.get('state',"") if cep.get('state') else ""
    #     campo_atual = _processa_campo_atual(json_coletas,'endereco_coleta',campos_endereco_entrega)



    #     if not campo_atual: 
    #         imprimirJsonTerminal(json_coletas['endereco_coleta'])
    #         json_coletas['pergunta'] =  dict_verificacao['pergunta_final']
    #         return json_coletas
        
    #     json_coletas['pergunta'] =  dict_verificacao[campo_atual]
    #     return json_coletas

    # campo_atual = _processa_campo_atual(json_coletas,'endereco_coleta',campos_endereco_entrega)

    # proximo_campo = _processa_proximo_campo(json_coletas, 'endereco_coleta', campos_endereco_entrega, campo_atual)

    # if campo_atual:
    #     if not proximo_campo:
    #         json_coletas['pergunta'] =  dict_verificacao['pergunta_final']
    #         json_coletas['endereco_coleta'][campo_atual] = msg
    #         return json_coletas
    #     else:
    #         json_coletas['pergunta'] =  dict_verificacao[proximo_campo]
    #         json_coletas['endereco_coleta'][campo_atual] = msg
    #         return json_coletas


    # if not campo_atual and json_coletas['endereco_coleta']['state'] == "aguardando":
    #     match msg:
    #         case 'editar':
    #             json_coletas['endereco_coleta']['state'] = 'editando'
    #             json_coletas['pergunta'] = "Qual dado você deseja alterar? (1) CEP, (2) Rua, (3) Número, (4) Complemento, (5) Bairro, (6) Cidade, (7) Estado."
    #         case 'ok':
    #             json_coletas['endereco_coleta']['state'] = 'finalizado'
    #             json_coletas['pergunta'] = "Ótimo! Agora me passa o CEP da coleta, por favor!"
    #     return json_coletas
    
    # if json_coletas['endereco_coleta']['state'] == "editando":
    #     match msg:
    #         case '1':
    #             json_coletas['endereco_coleta']['cep'] = ''
    #             json_coletas['endereco_coleta']['state'] = 'aguardando'
    #             json_coletas['pergunta'] = "Me passa o CEP da coleta, por favor!"
    #             return json_coletas

    #         case '2':
    #             json_coletas['endereco_coleta']['rua'] = ''
    #             json_coletas['endereco_coleta']['state'] = 'aguardando'
    #             json_coletas['pergunta'] = "E a rua, qual é?"
    #             return json_coletas
    #         case '3':
    #             json_coletas['endereco_coleta']['num'] = ''
    #             json_coletas['endereco_coleta']['state'] = 'aguardando'
    #             json_coletas['pergunta'] = "Agora me fala o número do endereço."
    #             return json_coletas
    #         case '4':
    #             json_coletas['endereco_coleta']['complemento'] = ''
    #             json_coletas['endereco_coleta']['state'] = 'aguardando'
    #             json_coletas['pergunta'] = "Tem algum complemento? Se não tiver, só digita 'não'."
    #             return json_coletas
    #         case '5':
    #             json_coletas['endereco_coleta']['bairro'] = ''
    #             json_coletas['endereco_coleta']['state'] = 'aguardando'
    #             json_coletas['pergunta'] = "E o bairro, qual é?"
    #             return json_coletas

    #         case '6':
    #             json_coletas['endereco_coleta']['cidade'] = ''
    #             json_coletas['endereco_coleta']['state'] = 'aguardando'
    #             json_coletas['pergunta'] = "Agora me diz a cidade."
    #             return json_coletas

    #         case '7':
    #             json_coletas['endereco_coleta']['uf'] = ''
    #             json_coletas['endereco_coleta']['state'] = 'aguardando'
    #             json_coletas['pergunta'] = "E qual é o estado?"
    #             return json_coletas

    #     return json_coletas

    # campos_vazios = [campo for campo, valor in json_coletas['endereco_coleta'].items() if valor == '']
    # if len(campos_vazios)>0:
    #     _processar_endereco_coleta(json_coletas,msg,'endereco_coleta')
    #     return json_coletas

    return json_coletas    


