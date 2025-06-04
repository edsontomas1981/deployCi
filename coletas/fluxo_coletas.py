from conexao import get_db,close_connection
from utils import documento_e_valido,remove_caracteres_cnpj_cpf,validar_cep
from clientes import get_cliente_by_cnpj,create_cliente
from cep import busca_cep
from coletas.campo_atual import get_campo_atual
from coletas.proximo_campo import get_proximo_campo
from coletas.processar_estado_coleta import processar_estado_coleta

def main_coletas(json_coletas,msg):
    # referente ao endereço de coleta
    if json_coletas['endereco_coleta']['state']=='gerando':

        dict_verificacao = {'cep': "Me passa o CEP da coleta, por favor!",
            'rua': "E a rua, qual é?",
            'num':"Agora me fala o número do endereço.",
            'complemento':  "Tem algum complemento? Se não tiver, só digita 'não'.",        
            'bairro':"E o bairro, qual é?",
            'cidade':  "Agora me diz a cidade.",
            'uf':"E qual é o estado?",
            'dados_coleta': 'dados_coleta',
            'pergunta_final':f"""Ótimo! Agora, confirme o endereco de coleta: CEP: {json_coletas['endereco_coleta']['cep']},Endereço: {json_coletas['endereco_coleta']['rua']}, Nº: {json_coletas['endereco_coleta']['num']}, Complemento: {json_coletas['endereco_coleta']['complemento']},Bairro: {json_coletas['endereco_coleta']['bairro']}, Cidade: {json_coletas['endereco_coleta']['cidade']}, Estado: {json_coletas['endereco_coleta']['uf']}.Está tudo correto ou deseja fazer alguma alteração? Digite 'editar' para modificar os dados ou 'ok' para prosseguir."""}
        
        campos_endereco_coleta = ['cep','rua','num','complemento','bairro','cidade','uf']

        campo_atual = get_campo_atual(json_coletas,'endereco_coleta',campos_endereco_coleta)

        if campo_atual == 'cep' and json_coletas['endereco_coleta']['cep']=='':
            if not validar_cep(msg):
                json_coletas['pergunta'] = "O CEP que você digitou não é válido. Por favor, digite um CEP válido."
                return json_coletas
            
            cep = busca_cep(msg)
            json_coletas['endereco_coleta']['cep'] = cep.get('cep') if cep.get('cep') else msg
            json_coletas['endereco_coleta']['rua'] = cep.get('street') if cep.get('street') else ""
            json_coletas['endereco_coleta']['bairro'] = cep.get('neighborhood') if cep.get('neighborhood') else ""
            json_coletas['endereco_coleta']['cidade'] = cep.get('city',"") if cep.get('city') else ""
            json_coletas['endereco_coleta']['uf'] = cep.get('state', "") if cep.get('state') else ""
    
            proximo_campo = get_proximo_campo(json_coletas, 'endereco_coleta', campos_endereco_coleta, campo_atual)

            json_coletas['pergunta'] = dict_verificacao[proximo_campo]
            return json_coletas

        campo_atual = get_campo_atual(json_coletas,'endereco_coleta',campos_endereco_coleta)

        proximo_campo = get_proximo_campo(json_coletas, 'endereco_coleta', campos_endereco_coleta, campo_atual)

        json_coletas['endereco_coleta'][campo_atual] = msg
        json_coletas['pergunta'] = dict_verificacao[proximo_campo] if proximo_campo else dict_verificacao['pergunta_final']

        if not proximo_campo:
            json_coletas['endereco_coleta']['state'] = 'aguardando'
        return json_coletas
    
    if json_coletas['endereco_coleta']['state'] == 'aguardando':
        return processar_estado_coleta(json_coletas, msg)






