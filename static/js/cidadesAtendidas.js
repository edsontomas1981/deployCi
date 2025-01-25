document.addEventListener('DOMContentLoaded',async ()=>{
    let dados = ordenarPorCidade(jsonCidades())
    popula_tbody_paginacao('navCidadesAtendidas','tbodyCidadesAtendidas',dados,false,1,20,false)
    let inptCidade = document.getElementById('inptBuscaCidade')

    inptCidade.addEventListener('input',()=>{
        let dadosFiltrados = buscarCidade(ordenarPorCidade(dados),inptCidade.value)
        popula_tbody_paginacao('navCidadesAtendidas','tbodyCidadesAtendidas',dadosFiltrados,false,1,20,false)
    })
})



