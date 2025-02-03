import json
from estados_contatos import get_estado_contato_by_telefone,create_estado_contato,update_estado_contato
# from coletas import Coletas

# Função para gerar o menu
def gerar_menu():
    menu = """
    ===== MENU =====
    1. Coletas
    2. Cotação
    3. Posição de Coletas
    4. Posição de Notas
    0. Sair
    
    Escolha uma opção enviando o número correspondente.
    """

    return menu

def selecao_menu(estado_contato,msg,telefone):
    print(type(estado_contato[4]))
    match str(estado_contato[4]):
        case "0":
            update_estado_contato(telefone,0,1,msg)
            return gerar_menu()
        case "1":
            match msg:
                case "1":
                    update_estado_contato(telefone,0,1,json.dumps({'msg':'Dados','text':'treo'}))
                    return "Coletas"
                case "2":
                    return f"Cotação"
                    # Ação para valor2
                case "3":
                    return "Coletas"
                case "4":
                    return f"Cotação"
                    # Ação para valor2
                case "5":
                    # Ação caso nenhum padrão seja correspondido
                    pass
