def obter_mensagem_pergunta(campo,mensagens):
    """Retorna a mensagem correspondente ao campo solicitado.
    mensagens = {
        'cep': "Me passa o CEP da coleta, por favor!",
        'rua': "E a rua, qual é?",
        'num': "Agora me fala o número do endereço.",
        'complemento': "Tem algum complemento? Se não tiver, só digita 'não'.",
        'bairro': "E o bairro, qual é?",
        'cidade': "Agora me diz a cidade.",
        'uf': "E qual é o estado?",
    }"""
    return mensagens.get(campo, "Qual informação deseja atualizar?")