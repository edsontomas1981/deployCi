btnIncluiCte.addEventListener('click',()=>{
    let item = cte.value; // Obtém o valor do item
    incluirCte(item)

})

btnBaixaCte.addEventListener('click',()=>{
    enviarLote()
})

function incluirCte(cteNum) {
    if (ctes.includes(cteNum)) {
        msgErro('Erro: O item já está na lista.');
    } else {
        ctes.push(cteNum); // Adiciona o item à lista
        cte.value = '';
        cte.focus();
        populaTabelaCtes()
    }
}

function preparaDadosTabela() {
    let listaCtes = []
    ctes.forEach((value, index) => {
        listaCtes.push({indice:index +1, valor:value});
    });
    return listaCtes
}

function populaTabelaCtes() {
    let dadosTabela = preparaDadosTabela()
    popula_tbody('tableCtes',dadosTabela,false,false)
}

// Adiciona um listener para o evento 'keydown'
cte.addEventListener('keydown', (event) => {
    // Verifica se a tecla Enter foi pressionada
    if (event.key === 'Enter') {
        let item = cte.value; // Obtém o valor do item
        incluirCte(item)
        console.log('A tecla Enter foi pressionada!');
        // Adicione aqui qualquer lógica adicional necessária
    }
});

btnLimpaListaCteNum.addEventListener('click',()=>{
    ctes = []
    populaTabelaCtes()
})

btnLimpaCteNum.addEventListener('click',()=>{
    cte.value = ''
    cte.focus()
})

document.addEventListener('keydown', (event) => {
    // Verifica se Ctrl e S foram pressionados simultaneamente
    if (event.ctrlKey && event.key === 'b' || event.ctrlKey && event.key === 'B') {
        enviarLote()
    }
});

function enviarLote() {
    // Verificar se existem CTes antes de continuar
    if (ctes.length === 0) {
        msgErro('🚨 Eita! Cadê os CTes? Você esqueceu de informar.');
        return;
    }

    // Confirmar a ação antes de iniciar o processo
    msgConfirmacao('📥 Você quer fazer o download dos documentos agora?').then((confirmado) => {
        if (confirmado) {
            showLoaderSweet('🚀 Segura aí! Estamos baixando seus arquivos rapidinho... 📂💨');
            // Instanciar o serviço de API
            let apiService = new ApiService(BASEURL);

            // Executar o processo de download
            apiService.downloadFile('baixar_ctes_lote', ctes)
                .then(() => {
                    hideLoaderSweet(); // Fechar o loader em caso de erro
                    Swal.fire('🎉 Sucesso!', 'Os arquivos foram baixados com sucesso! 😎', 'success');
                })
                .catch((error) => {
                    hideLoaderSweet(); // Fechar o loader em caso de erro
                    console.error('Erro ao baixar os arquivos:', error);
                    Swal.fire('❌ Oops!', 'Algo deu errado ao baixar os arquivos. Tente novamente. 🙁', 'error');
                });
        }
    });
}


