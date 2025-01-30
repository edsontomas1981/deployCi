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

        await apiService.downloadFile('baixar_coletas_lote', dados)
        .then(response => {            
            hideLoaderSweet();
    
            // Verifica se há detalhes na resposta
            if (response.detalhes) {
                const { arquivos_sucesso, arquivos_erro } = response.detalhes;
    
                console.log("Arquivo baixado:", response.arquivo);
                console.log("Arquivos gerados com sucesso:", arquivos_sucesso);
                console.log("Arquivos com erro:", arquivos_erro);
    
                // Se houver arquivos com erro, exibe a mensagem
                if (arquivos_erro.length > 0) {
                    const errosFormatados = arquivos_erro.map(erro => `📌 ${erro}`).join('<br>');
                    Swal.fire({
                        icon: 'warning',
                        title: '⚠️ Atenção!',
                        html: `Alguns arquivos apresentaram erro:<br><br>${errosFormatados}`,
                    });
                } else {
                    Swal.fire('🎉 Sucesso!', 'Os arquivos foram baixados com sucesso! 😎', 'success');
                }
    
                limpaLista();
            } else {
                // Caso a resposta não tenha os detalhes esperados
                Swal.fire('❌ Erro!', 'A resposta do servidor não está no formato esperado.', 'error');
            }
        })
        .catch(error => {
            console.error("Erro ao baixar:", error);
            Swal.fire('❌ Erro!', 'Ocorreu um erro ao baixar os arquivos.', 'error');
        });
   

    } catch (error) {
        console.error(`Erro ao baixar a coleta`, error);
        Swal.fire('❌ Oops!', 'Algo deu errado ao baixar os arquivos. Tente novamente. 🙁', 'error');
    }

    // Ocultar o loader após um breve intervalo
    setTimeout(hideLoader, 2000);

    const fim = performance.now();
    console.log(`Tempo gasto: ${(fim - inicio).toFixed(2)}ms`);

}
