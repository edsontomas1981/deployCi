from contatos import Contato

messages = {}

def carrega_contato(phone,nome):
    """Adiciona um contato ao dicionário 'messages' caso ainda não exista.

    Args:
        contato: Um objeto que deve ter um atributo 'phone' representando o número do contato.
    
    Returns:
        O contato existente, se já estiver cadastrado, ou o novo contato adicionado.
    """

    if phone in messages:
        print("O contato já existe.")
        return messages[phone]  # Retorna o contato já existente
    
    contato = add_contato(phone,nome)

    print(f"Contatos: {messages}")

    return contato  # Retorna o novo contato adicionado


def add_contato(contato,nome):
    contato=Contato(contato, nome)
    messages[contato.phone] = contato
    print(f"Contatos: {messages}")
    return contato
