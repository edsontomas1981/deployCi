const populaCi = (dados)=>{
  let isca1 = document.getElementById('isca1')
  let isca2 = document.getElementById('isca2')
  let manifesto = document.getElementById('numManifesto')
  let frete = document.getElementById('freteValor')
  let destinatario = document.getElementById('destinatario')
  let motorista = document.getElementById('motorista')
  let dataCi = document.getElementById('dataCi')
  let observacao = document.getElementById('observacao')
  let rota = document.getElementById('rota')
  let idNumCi = document.getElementById('idCiNum')

  isca1.value = dados.isca_1
  isca2.value = dados.isca_2
  manifesto.value = dados.manifesto_numero
  destinatario.value = dados.destinatario
  frete.value = dados.valor_frete
  motorista.value = dados.motorista
  dataCi.value = formatarData(dados.data)
  observacao.value = dados.observacao
  rota.value = dados.percurso
  idNumCi.value = dados.ci_num
}

const limpaForm = ()=>{
    let isca1 = document.getElementById('isca1')
    let isca2 = document.getElementById('isca2')
    let manifesto = document.getElementById('numManifesto')
    let frete = document.getElementById('freteValor')
    let destinatario = document.getElementById('destinatario')
    let motorista = document.getElementById('motorista')
    let dataCi = document.getElementById('dataCi')
    let observacao = document.getElementById('observacao')
    let rota = document.getElementById('rota')
    let idCi = document.getElementById('idCiNum')
    let ciNum = document.getElementById('ciNum')
    
    isca1.value = ''
    isca2.value = ''
    manifesto.value = ''
    destinatario.value = ''
    frete.value = ''
    motorista.value = ''
    dataCi.value = ''
    observacao.value = ''
    rota.value = ''
    idCi.value = ''
    ciNum.value = ''
}

const salvaCi = (dadosCi)=>{
  let apiService = new ApiService(BASEURL);
  apiService.create('comunicacao', dadosCi)
  .then(data => verificaSalvar(data))
  .catch(error => console.error('Error:', error));
}

const updateCi = (dadosCi,idCi)=>{
  msgConfirmacao(`Deseja Atualizar a Comunicação Interna de nº ${idCi}?`).then((confirmado) => {
    if (confirmado) {
      let apiService = new ApiService(BASEURL);
      // Deletar uma comunicação
      apiService.update('comunicacao',idCi,dadosCi)
          .then(data => verificaSalvar())
          .catch(error => console.error('Error:', error));
    }
  });
}

let btnSalvar = document.getElementById('salvar')
btnSalvar.addEventListener('click',()=>{
  let isca1 = document.getElementById('isca1')
  let isca2 = document.getElementById('isca2')
  let manifesto = document.getElementById('numManifesto')
  let frete = document.getElementById('freteValor')
  let destinatario = document.getElementById('destinatario')
  let motorista = document.getElementById('motorista')
  let dataCi = document.getElementById('dataCi')
  let observacao = document.getElementById('observacao')
  let rota = document.getElementById('rota')
  // Criar uma nova comunicação
  const dadosCi = {
      destinatario: destinatario.value,
      manifesto_numero: manifesto.value,
      motorista: motorista.value,
      valor_frete: frete.value,
      percurso: rota.value,
      data: dataCi.value,
      observacao: observacao.value,
      isca_1: isca1.value,
      isca_2: isca2.value
  };

  if (document.getElementById('idCiNum').value != ''){
    updateCi(dadosCi,document.getElementById('idCiNum').value)
  }else{
    salvaCi(dadosCi)
  }

})

const imprimirCi = async(element)=>{
  msgConfirmacao(`Deseja Imprimir a Comunicação Interna de nº ${element}?`).then((confirmado) => {
    if (confirmado) {
      // Exemplo de uso:
      const apiService = new ApiService(BASEURL);

      apiService.getById('comunicacao', element)
      .then(data => reportCi(data))
      .catch(error => console.error('Error:', error));
    }
  });
} 



const buscaCi = (idCi)=>{
  let apiService = new ApiService(BASEURL);
  // Obter uma comunicação por ID
  apiService.getById('comunicacao',idCi)
    .then(data => populaCi(data))
    .catch(error => console.error('Error:', error));
}

let btnBuscar = document.getElementById('buscar')
btnBuscar.addEventListener('click',()=>{
  buscaCi(document.getElementById('ciNum').value)
})

const verificaSalvar= (dados)=>{
    carregaTbody()
    limpaForm()
}

const deletaCi = (idCi)=>{
  msgConfirmacao(`Deseja Excluir a Comunicação Interna de nº ${idCi}?`).then((confirmado) => {
    if (confirmado) {
      let apiService = new ApiService(BASEURL);
      // Deletar uma comunicação
      apiService.delete('comunicacao',idCi)
          .then(data => handlerExcuir())
          .catch(error => console.error('Error:', error));
    }
  });
}

const handlerDeleteCi = (idCi)=>{
  deletaCi(idCi)
}

const handlerBuscaCi = (idCi)=>{
  buscaCi(idCi)
}

const carregaTbody = async ()=>{
    let apiService = new ApiService(BASEURL);

    let botoes={
      print:{
          classe: "btn btn-info text-white btn-table",
          texto: '<i class="fa fa-print" aria-hidden="true"></i>',
          callback: imprimirCi
      },
      excluir:{
          classe: "btn btn-danger text-white btn-table",
          texto: '<i class="fa fa-trash" aria-hidden="true"></i>',
          callback: handlerDeleteCi
          },
      buscar:{
        classe: "btn btn-primary text-white btn-table",
        texto: '<i class="fa fa-search" aria-hidden="true"></i>',
        callback: handlerBuscaCi
        }          
      }; 

      // Obter todas as comunicações
      var dados = await apiService.getAll('comunicacoes')
      .then(data => transformarEmListaDeListas(data))
      .catch(error => console.error('Error:', error))

      popula_tbody_paginacao('paginacao','dadosCi',dados,botoes,1,20,false)

  }

const handlerExcuir = ()=>{
    limpaForm()
    carregaTbody()
    msgAviso('CI Deletada com Sucesso!')
}

document.getElementById('excluir').addEventListener('click',()=>{
  if(document.getElementById('idCiNum').value != ""){
    deletaCi(document.getElementById('idCiNum').value)
  }
})

document.getElementById('btnPrintCi').addEventListener('click',()=>{
  if(document.getElementById('idCiNum').value != ""){
    imprimirCi(document.getElementById('idCiNum').value)
  }
})

document.getElementById('limparForm').addEventListener('click',()=>{
  limpaForm()
})

document.addEventListener('DOMContentLoaded',()=>{
    tippy('[data-tippy-content]', {
      placement: 'top', // Posição do tooltip: top, bottom, left, right
      animation: 'fade', // Tipo de animação
      theme: 'light', // Tema personalizado (opcional)
    }); 
    carregaTbody()
})

