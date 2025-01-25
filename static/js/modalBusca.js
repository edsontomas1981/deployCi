document.getElementById('btnPesquisa').addEventListener('click',()=>{
  
    let dados = {}

    if (document.getElementById('termoObs').value != ''){
        dados.observacao=document.getElementById('termoObs').value
    }

    if (document.getElementById('termoPercurso').value != ''){
        dados.percurso=document.getElementById('termoPercurso').value
    }

    if (document.getElementById('termoIsca').value != ''){
        dados.isca=document.getElementById('termoIsca').value
    }

    if (document.getElementById('termoMotorista').value != ''){
        dados.motorista=document.getElementById('termoMotorista').value
    }

    const api = new ApiService(BASEURL);
    // Busca com filtros
    api.search('selecionar_ci', {
        dados
    }).then(result => {
      populaTabelaModal(result);
    }).catch(error => {
        console.error("Erro ao buscar:", error.message);
    });
})

const limpaModal = ()=>{
  document.getElementById('termoObs').value =''
  document.getElementById('termoPercurso').value =''
  document.getElementById('termoIsca').value =''
  document.getElementById('termoMotorista').value =''
  document.getElementById('dadosCiModal').innerHTML = ''
  document.getElementById('paginacaoModal').innerHTML = ''

}

const fecharModal = () => {
  const modalElement = document.querySelector('#modalBuscaAvancada'); // Substitua pelo ID do modal
  const modalInstance = bootstrap.Modal.getInstance(modalElement);
  limpaModal()
  modalInstance.hide();
};

const handlerDeleteCiModal = async (e)=>{
  buscaCi(e)
  fecharModal(); 
}

const populaTabelaModal = (dados)=>{
    let botoes={
      print:{
          classe: "btn btn-info text-white",
          texto: '<i class="fa fa-print" aria-hidden="true"></i>',
          callback: imprimirCi
      },
      buscar: {
        classe: "btn btn-primary text-white",
        texto: '<i class="fa fa-search" aria-hidden="true"></i>',
        callback:handlerDeleteCiModal
      }         
    }; 

    let dadosNormatizados = normalizaDados(dados)

    
    popula_tbody_paginacao('paginacaoModal','dadosCiModal',dadosNormatizados,botoes,1,10,false)
}

const normalizaDados = (dados)=>{
  // Criar uma lista vazia para armazenar as listas de objetos
  const listaDeListas = [];

  // Iterar sobre cada objeto na lista de dados
  for (const objeto of dados) {
    // Criar uma nova lista para armazenar as propriedades do objeto
    const listaDePropriedades = [];

    // Iterar sobre cada chave do objeto
    for (const chave in objeto) {
      // Adicionar o valor da chave à lista de propriedades
      listaDePropriedades.push(objeto[chave]);
    }

    // Adicionar a lista de propriedades à lista de listas
    listaDeListas.push(listaDePropriedades);
  }

  // Retornar a lista de listas
  return listaDeListas;
}


