let btnBaixar = document.getElementById('baixar');
let mensagemDeCarga = document.getElementById('mensagemDeCarga');

// Evento do botão para baixar coletas
btnBaixar.addEventListener('click', async () => {
    // Medindo o tempo gasto
    const inicio = performance.now();
    let apiService = new ApiService(BASEURL);
    
    // Mostrar loader com a mensagem inicial
    showLoader("Iniciando o download das coletas, por favor aguarde...");
    
    const dados = getWordsFromTextarea("coletas");
    const totalPedidos = dados.length;
    
    if (totalPedidos === 0) {
        showLoader("Nenhuma coleta encontrada. Verifique os dados e tente novamente.");
        setTimeout(hideLoader, 2000);
        return;
    }

    // Configuração inicial da barra de progresso
    const passo = 100 / totalPedidos; // Progresso por pedido
    let progressoAtual = 0;
    updateProgressBar(progressoAtual);

    // Processar cada coleta
    for (const [index, coleta] of dados.entries()) {
        // Atualizar a mensagem de carga para o pedido atual
        showLoader(`Tarefa ${index + 1}/${totalPedidos}: Baixando coleta ${coleta}, por favor aguarde...`);

        try {
            // Enviar a solicitação para a API
            let response = await apiService.create('get_coletas', coleta);
            console.log(response);

            // Atualizar o progresso
            progressoAtual += passo;
            updateProgressBar(progressoAtual);
        } catch (error) {
            console.error(`Erro ao baixar a coleta ${coleta}:`, error);
            showLoader(`Erro ao baixar a coleta ${coleta}. Continuando...`);
        }
    }

    // Garantir que a barra atinja 100% ao final
    updateProgressBar(100);
    showLoader("Todas as coletas foram baixadas com sucesso!");

    // Ocultar o loader após um breve intervalo
    setTimeout(hideLoader, 2000);

    const fim = performance.now();
    console.log(`Tempo gasto: ${(fim - inicio).toFixed(2)}ms`);

});


let btnBaixarLote = document.getElementById('baixarLote');

// Evento do botão para baixar coletas
btnBaixarLote.addEventListener('click', async () => {
    const inicio = performance.now();

    let apiService = new ApiService(BASEURL);
    
    // Mostrar loader com a mensagem inicial
    showLoader("Iniciando o download das coletas, por favor aguarde...");
    
    const dados = getWordsFromTextarea("coletas");
    const totalPedidos = dados.length;
    
    if (totalPedidos === 0) {
        showLoader("Nenhuma coleta encontrada. Verifique os dados e tente novamente.");
        setTimeout(hideLoader, 2000);
        return;
    }

    // Configuração inicial da barra de progresso
    const passo = 100 / totalPedidos; // Progresso por pedido
    let progressoAtual = 0;
    updateProgressBar(progressoAtual);

    try {
        // Enviar a solicitação para a API
        let response = await apiService.create('baixar_coletas_lote', dados);

        updateProgressBar(progressoAtual);
    } catch (error) {
        console.error(`Erro ao baixar a coleta ${coleta}:`, error);
        showLoader(`Erro ao baixar a coleta ${coleta}. Continuando...`);
    }

    // Garantir que a barra atinja 100% ao final
    updateProgressBar(100);
    showLoader("Todas as coletas foram baixadas com sucesso!");

    // Ocultar o loader após um breve intervalo
    setTimeout(hideLoader, 2000);

    const fim = performance.now();
    console.log(`Tempo gasto: ${(fim - inicio).toFixed(2)}ms`);

});


