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
    match estado_contato[1]:
        case "0":
            update_estado_contato(telefone,1,1,json.dumps({'msg':'Dados','text':'treo'}))
            return gerar_menu()
        case "1":
                match msg:
                    case "1":
                        dados = {"remetente":{"cnpj":'',"razao":'','cep':'','rua':'','numero':'','complemento':'','bairro':'','cidade':'','uf':'','state':'aguardando'},
                                "destinatario":{"cnpj":'',"razao":'','cep':'','rua':'','numero':'','complemento':'','bairro':'','cidade':'','uf':''},
                                "dados_coleta":{'volumes':'','peso':'','m3':'','valor_nf':'','num_nf':'','confirmacao':False},
                                "contato":{'telefone':'','nome':''},
                                "observacao":'',
                                "endereco_coleta":{'cep':'','rua':'','num':'','complemento':'',
                                                    'bairro':'','cidade':'','uf':'','state':'gerando'},
                                "endereco_entrega":{'cep':'','rua':'','num':'','complemento':'',
                                                    'bairro':'','cidade':'','uf':'','state':'gerando'},
                                "pergunta": "Me passa o CNPJ do remetente."
                                }
                        update_estado_contato(telefone,2,0,json.dumps(dados))
                        return "Beleza! Primeiro, me passa o CEP de onde a mercadoria será coletada."
                    case "2":
                        update_estado_contato(telefone,3,0,json.dumps({'msg':'Dados','text':'treo'}))
                        return f"Cotação"
                        # Ação para valor2
                    case "3":
                        update_estado_contato(telefone,4,0,json.dumps({'msg':'Dados','text':'treo'}))                        
                        return f"Posição Coletas"
                    case "4":
                        update_estado_contato(telefone,5,0,json.dumps({'msg':'Dados','text':'treo'}))                        
                        return f"Cotação"

                    case "0":
                        update_estado_contato(telefone,1,1,json.dumps({'msg':'Dados','text':'treo'}))
                        return gerar_menu()

                    case _:
                        return "Opção inválida. Por favor, escolha uma opção válida."