# from obter_mensagem_pergunta import obter_mensagem_pergunta

def processar_estado_coleta(json_coletas, msg):
    """Gerencia o estado da coleta e edições."""

    mensagens = {
        'cep': "Me passa o CEP da coleta, por favor!",
        'rua': "E a rua, qual é?",
        'num': "Agora me fala o número do endereço.",
        'complemento': "Tem algum complemento? Se não tiver, só digita 'não'.",
        'bairro': "E o bairro, qual é?",
        'cidade': "Agora me diz a cidade.",
        'uf': "E qual é o estado?",
    }

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
            # json_coletas['pergunta'] = obter_mensagem_pergunta(campo,mensagens)
    
    return json_coletas