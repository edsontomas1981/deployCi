// Adiciona um listener para o evento 'keydown'
inptColeta.addEventListener('keydown', (event) => {
    // Verifica se a tecla Enter foi pressionada
    if (event.key === 'Enter') {
        let item = inptColeta.value; // Obtém o valor do item
        incluirColeta(item)
        console.log('A tecla Enter foi pressionada!');
        // Adicione aqui qualquer lógica adicional necessária
    }
});

btnDownloadColeta.addEventListener('click',()=>{
    baixarColetas()
})

btnIncluiColeta.addEventListener('click',()=>{
    let item = inptColeta.value; // Obtém o valor do item
    incluirColeta(item)
})

function incluirColeta(coletaNum) {
    if (listaColetas.includes(coletaNum)) {
        msgErro('Erro: O item já está na lista.');
    } else {
        listaColetas.push(coletaNum); // Adiciona o item à lista
        inptColeta.value = '';
        inptColeta.focus();
        populaTabelaColetas()
    }
}

function limpaLista() {
    listaColetas = []
    populaTabelaColetas()
}

btnLimpaListaColeta.addEventListener('click',()=>{
    limpaLista()
})

btnLimpaColetaNum.addEventListener('click',()=>{
    inptColeta.value = ''
    inptColeta.focus()
})

function preparaDadosTabelaColetas() {
    let listaPreparadaColetas = []
    listaColetas.forEach((value, index) => {
        listaPreparadaColetas.push({indice:index +1, valor:value});
    });
    return listaPreparadaColetas
}

function populaTabelaColetas() {
    let dadosTabela = preparaDadosTabelaColetas()
    popula_tbody('tableColetas',dadosTabela,false,false)
}

document.addEventListener('keydown', (event) => {
    // Verifica se Ctrl e S foram pressionados simultaneamente
    if (event.ctrlKey && event.key === 'b' || event.ctrlKey && event.key === 'B') {
        baixarColetas()
    }
});

async function baixarColetas() {

    // Verificar se existem CTes antes de continuar
    if (listaColetas.length === 0) {
        msgErro('🚨 Eita! Cadê as Coletas? Você esqueceu de informar.');
        return;
    }

    const inicio = performance.now();

    let apiService = new ApiService(BASEURL);
    
    // Mostrar loader com a mensagem inicial
    showLoaderSweet('🚀 Segura aí! Estamos baixando seus arquivos rapidinho... 📂💨');
    
    const dados = listaColetas;
    
    try {
        // Enviar a solicitação para a API
        let response = await apiService.downloadFile('baixar_coletas_lote', dados);
        hideLoaderSweet()
        Swal.fire('🎉 Sucesso!', 'Os arquivos foram baixados com sucesso! 😎', 'success');
        limpaLista()

    } catch (error) {
        console.error(`Erro ao baixar a coleta ${coleta}:`, error);
        Swal.fire('❌ Oops!', 'Algo deu errado ao baixar os arquivos. Tente novamente. 🙁', 'error');
    }

    // Ocultar o loader após um breve intervalo
    setTimeout(hideLoader, 2000);

    const fim = performance.now();
    console.log(`Tempo gasto: ${(fim - inicio).toFixed(2)}ms`);
    
}