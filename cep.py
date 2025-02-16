from utils import busca_cep_ws,remove_caracteres_cep

def busca_cep(cep):
    cep = remove_caracteres_cep(cep)
    status, json_cep = busca_cep_ws(cep)
    if status == 200:
        return json_cep
    
    