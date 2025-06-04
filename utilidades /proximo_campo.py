def get_proximo_campo(json_coletas,entidade, campos, campo_atual):
    for campo in campos:
        if json_coletas[entidade][campo] == '' and campo != campo_atual :
            return campo
    return None