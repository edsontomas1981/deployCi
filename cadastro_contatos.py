from estados_contatos import get_estado_contato_by_telefone,create_estado_contato,update_estado_contato

def cadastrar_contatos(passo,telefone,mensagem):
    match passo[4]:
        case 1:
            update_estado_contato(telefone,1,2,mensagem)
            return f"Maravilha agora me informe seu nome"
        case 2:
            update_estado_contato(telefone,0,0,mensagem)
            return f"Olá {mensagem},em que posso te ajudar"
            # Ação para valor2
        case _:
            # Ação caso nenhum padrão seja correspondido
            pass