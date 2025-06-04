const jsonCidades = async ()=> {
    let apiService = new ApiService(BASEURL);
    let cidades = await apiService.getAll('listar_cidades_atendidas');
    cidades = cidades.map(cidade => {
        return [cidade.id,cidade.cidade,cidade.filial_responsavel]
    });
    return cidades
}

const buscarCidadeId = async (id)=> {
    let apiService = new ApiService(BASEURL);
    let cidade = await apiService.getById('listar_cidades_atendidas',id);
    return cidade
}
