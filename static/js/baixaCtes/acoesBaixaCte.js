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
    limpaListaCtes()
})

function limpaListaCtes(){
    ctes = []
    populaTabelaCtes()
}

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

async function enviarLote() {
    // Verificar se existem CTes antes de continuar
    if (ctes.length === 0) {
        msgErro('🚨 Eita! Cadê os CTes? Você esqueceu de informar.');
        return;
    }

    try {

        showLoaderSweet('🚀 Segura aí! Estamos baixando seus arquivos rapidinho... 📂💨');

        let apiService = new ApiService(BASEURL);

        await apiService.downloadFile('baixar_ctes_lote', ctes)
        .then(response => {
            hideLoaderSweet();

            // Verifica se há detalhes na resposta
            // if (response.detalhes) {

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

            limpaListaCtes();
            // }
            //  else {
            //     // Caso a resposta não tenha os detalhes esperados
            //     Swal.fire('❌ Erro!', 'A resposta do servidor não está no formato esperado.', 'error');
            // }
        })
        .catch(error => {
            console.error("Erro ao baixar:", error);
            Swal.fire('❌ Erro!', 'Ocorreu um erro ao baixar os arquivos.', 'error');
        });


    } catch (error) {
        console.error(`Erro ao baixar a coleta`, error);
        Swal.fire('❌ Oops!', 'Algo deu errado ao baixar os arquivos. Tente novamente. 🙁', 'error');
    }

    // // Verifica se há detalhes na resposta
    // if (response.detalhes) {
    //     const { arquivos_sucesso, arquivos_erro } = response.detalhes;

    //     console.log("Arquivo baixado:", response.arquivo);
    //     console.log("Arquivos gerados com sucesso:", arquivos_sucesso);
    //     console.log("Arquivos com erro:", arquivos_erro);

    //     // Se houver arquivos com erro, exibe a mensagem
    //     if (arquivos_erro.length > 0) {
    //         const errosFormatados = arquivos_erro.map(erro => `📌 ${erro}`).join('<br>');
    //         Swal.fire({
    //             icon: 'warning',
    //             title: '⚠️ Atenção!',
    //             html: `Alguns arquivos apresentaram erro:<br><br>${errosFormatados}`,
    //         });
    //     } else {
    //         Swal.fire('🎉 Sucesso!', 'Os arquivos foram baixados com sucesso! 😎', 'success');
    //     }

    //     limpaLista();
    // } else {
    //     // Caso a resposta não tenha os detalhes esperados
    //     Swal.fire('❌ Erro!', 'A resposta do servidor não está no formato esperado.', 'error');
    // }

    // // Confirmar a ação antes de iniciar o processo
    // msgConfirmacao('📥 Você quer fazer o download dos documentos agora?').then((confirmado) => {
    //     if (confirmado) {
    //         showLoaderSweet('🚀 Segura aí! Estamos baixando seus arquivos rapidinho... 📂💨');
    //         // Instanciar o serviço de API
    //         let apiService = new ApiService(BASEURL);


    //         // Executar o processo de download
    //         let response = apiService.downloadFile('baixar_ctes_lote', ctes)
    //             .then(() => {
    //                 hideLoaderSweet(); // Fechar o loader em caso de erro
    //                 concole.log(response)
    //                 Swal.fire('🎉 Sucesso!', 'Os arquivos foram baixados com sucesso! 😎', 'success');
    //             })
    //             .catch((error) => {
    //                 hideLoaderSweet(); // Fechar o loader em caso de erro
    //                 console.error('Erro ao baixar os arquivos:', error);
    //                 Swal.fire('❌ Oops!', 'Algo deu errado ao baixar os arquivos. Tente novamente. 🙁', 'error');
    //             });
    //     }
    // });
}
