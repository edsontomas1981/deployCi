def get_campo_atual(json_coletas,entidade, campos):
    for campo in campos:
        print(f'Campo: {campo} valor do campo:{json_coletas[entidade][campo]} ')
        if json_coletas[entidade][campo] == '' or not json_coletas[entidade][campo]:
            return campo
    return None