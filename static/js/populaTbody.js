const truncateString=(str, maxLength)=> {
  return str.length > maxLength ? str.substring(0, maxLength) + '...' : str;
}
/**
 * Cria um elemento de botão de paginação para ser usado em um componente de paginação.
 * @param {string} iconClass - A classe do ícone a ser exibido no botão (opcional).
 * @param {number} page - O número da página associado ao botão.
 * @param {number} totalPages - O número total de páginas disponíveis.
 * @param {boolean} [isActive=false] - Indica se o botão deve ser destacado como ativo (padrão é falso).
 * @param {string} divParaNavegacao - O ID da div que contém a tabela a ser paginada.
 * @param {string} idTbody - O ID do corpo da tabela a ser populado com os dados.
 * @param {Array} dados - Os dados a serem exibidos na tabela paginada.
 * @param {Object} botoes - Um objeto contendo definições de botões personalizados.
 * @param {number} [itensPorPagina=10] - O número de itens a serem exibidos por página (padrão é 10).
 * @returns {HTMLLIElement} - Um elemento li contendo o botão de paginação.
 */
const createPaginationButton = (iconClass, page, totalPages, isActive = false, divParaNavegacao, idTbody, dados, botoes,itensPorPagina = 10) => {
  const li = document.createElement("li");
  li.className = `page-item ${isActive ? "active" : ""}`;

  const a = document.createElement("a");
  a.className = "page-link";
  if (iconClass) {
    const icon = document.createElement("i");
    icon.className = iconClass;
    a.appendChild(icon);
  } else {
    a.textContent = page;
  }

  if (page > 0 && page <= totalPages) {
    a.addEventListener("click", function () {
      // Certifique-se de que 'dados' e 'botoes' estejam no escopo correto
      popula_tbody_paginacao(divParaNavegacao, idTbody, dados, botoes, page,itensPorPagina,true,false);
    });
  }

  li.appendChild(a);
  return li;
  
};

/**
 * Preenche o corpo de uma tabela com dados paginados e adiciona controles de paginação.
 * @param {string} divParaNavegacao - O ID da div serão colocados os botoes da navegação.
 * @param {string} id_tbody - O ID do corpo da tabela a ser populado com os dados.
 * @param {Array} dados - Os dados a serem exibidos na tabela paginada.
 * @param {Object} [botoes={}] - Um objeto contendo definições de botões personalizados.
 * @param {number} [paginaAtual=1] - O número da página atual (padrão é 1).
 * @param {number} [itensPorPagina=10] - O número de itens a serem exibidos por página (padrão é 10).
 */
const popula_tbody_paginacao = async (divParaNavegacao, id_tbody, dados, botoes = {}, paginaAtual = 1, itensPorPagina = 10,dadosAdicionais = false) => {

  // Calcula o índice inicial e final dos dados a serem exibidos na página atual
  const startIndex = (paginaAtual - 1) * itensPorPagina;
  const endIndex = startIndex + itensPorPagina;

  // Filtra os dados para exibir apenas os dados da página atual
  const dadosPaginados = dados.slice(startIndex, endIndex);

  // Obtém a referência ao corpo da tabela
  var tbody = document.getElementById(id_tbody);
  // Limpa o conteúdo atual da tabela
  limpa_tabelas(id_tbody);

  dadosPaginados.forEach(element => { 
    var tr = document.createElement("tr");
    tr.setAttribute('data-id', element[0]);
    // Loop através do dicionário de dados para criar as células <td> dinamicamente
    for (const chave in element) {
      if (element.hasOwnProperty(chave)) {
        var td = document.createElement("td");

        // Verificar se o valor associado à chave é um objeto (hashTable)
        if (typeof element[chave] === 'object' && element[chave] !== null) {
          // Se for um objeto, você pode adicionar a lógica desejada aqui
          // td.textContent = 'É uma hashTable';
        } else {
          // Caso contrário, apenas atribua o valor normalmente
          td.textContent = element[chave] ? truncateString(element[chave], 15) : "Sem informação";
        }

        tr.appendChild(td);
      }
    }
    // Adiciona botões personalizados se existirem na hash 'botoes'
    for (const nomeBotao in botoes) {
      if (botoes.hasOwnProperty(nomeBotao)) {
        var tdBotao = document.createElement("td");
        var btn = document.createElement("a");
        btn.setAttribute('data-id', element[0]);

        btn.id = element[0];
        btn.className = "btn btn-sm " + botoes[nomeBotao].classe;
        btn.innerHTML = botoes[nomeBotao].texto;
  
        if (botoes[nomeBotao].callback) {
          // Use uma função anônima para passar o ID
          btn.onclick = function() {
            // Chame a função de callback passando o ID
            botoes[nomeBotao].callback(element[0]);
          };
        }
        tdBotao.appendChild(btn);
        tr.appendChild(tdBotao);
      }
    }
    tbody.appendChild(tr);
  });
  

  // Remove qualquer elemento de paginação existente
  var existingPagination = document.querySelector('.pagination');
  if (existingPagination) {
    existingPagination.remove();
  }

  // Calcula o número total de páginas com base no número total de dados e itens por página
  const totalPages = Math.ceil(dados.length / itensPorPagina);
  // Cria o contêiner de paginação
  const paginationContainer = document.createElement("ul");
  paginationContainer.className = "pagination flex-wrap";

  // Adiciona botão "Anterior" à paginação
  const previousButton = createPaginationButton("fa fa-arrow-left", paginaAtual - 1, totalPages, false, divParaNavegacao, id_tbody, dados, botoes, itensPorPagina);
  paginationContainer.appendChild(previousButton);

  // Adiciona botões numéricos à paginação
  for (let i = 1; i <= totalPages; i++) {
    const numericButton = createPaginationButton(null, i, totalPages, i === paginaAtual, divParaNavegacao, id_tbody, dados, botoes, itensPorPagina);
    paginationContainer.appendChild(numericButton);
  }

  // Adiciona botão "Próximo" à paginação
  const nextButton = createPaginationButton("fa fa-arrow-right", paginaAtual + 1, totalPages, false, divParaNavegacao, id_tbody, dados, botoes, itensPorPagina);
  paginationContainer.appendChild(nextButton);

  // Adiciona o elemento de paginação à div de navegação
  document.getElementById(divParaNavegacao).appendChild(paginationContainer);
};


/**
 * Adiciona botões personalizados a uma linha de tabela se existirem na hash 'botoes'.
 * @param {Object} element - Objeto representando os dados da linha da tabela.
 * @param {Object} botoes - Hash contendo informações sobre os botões personalizados a serem adicionados.
 * @param {string} botoes[nomeBotao].classe - Classe CSS a ser aplicada ao botão.
 * @param {string} botoes[nomeBotao].texto - Texto a ser exibido no botão.
 * @param {function} botoes[nomeBotao].callback - Função de callback a ser chamada quando o botão é clicado.
 */




/**
 * Preenche o corpo de uma tabela com dados e adiciona botões personalizados.
 * @param {string} id_tbody - O ID do corpo da tabela a ser populado com os dados.
 * @param {Array} dicionario_dados - O array de objetos contendo os dados a serem exibidos na tabela.
 * @param {Object} [botoes={}] - Um objeto contendo definições de botões personalizados.
 * @example
 * // Exemplo de chamada da função com botões personalizados
 * popula_tbody('tabelaCorpo', dados, {
 *   editar: {
 *     classe: 'btn-primary',
 *     texto: 'Editar',
 *     callback: function(id) {
 *       console.log('Botão Editar clicado para o ID:', id);
 *     }
 *   },
 *   excluir: {
 *     classe: 'btn-danger',
 *     texto: 'Excluir',
 *     callback: function(id) {
 *       console.log('Botão Excluir clicado para o ID:', id);
 *     }
 *   }
 * });
 */
const popula_tbody = (id_tbody, dicionario_dados, botoes = {},inicioChebox=true) => {
  console.log(dicionario_dados)

  // Obtém a referência ao elemento tbody da tabela
  var tbody = document.getElementById(id_tbody);

  // Limpa o conteúdo atual da tabela
  limpa_tabelas(id_tbody);


  // Itera sobre os dados para criar linhas na tabela
  dicionario_dados.forEach(element => {
    var tr = document.createElement("tr");
    tr.setAttribute('data-id', element.id);
    if(inicioChebox){
      // Adiciona o checkbox como o primeiro campo
      var tdCheckbox = document.createElement("td");
      var checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.name = "selecao";
      tdCheckbox.appendChild(checkbox);
      tr.appendChild(tdCheckbox);
    }

    // Loop através do dicionário de dados para criar as células <td> dinamicamente
    for (const chave in element) {
      if (element.hasOwnProperty(chave)) {
        var td = document.createElement("td");
        td.textContent = element[chave];
        tr.appendChild(td);
      }
    }

    // Adiciona botões personalizados se existirem na hash 'botoes'
    for (const nomeBotao in botoes) {
      if (botoes.hasOwnProperty(nomeBotao)) {
        var tdBotao = document.createElement("td");
        var btn = document.createElement("a");
        btn.setAttribute('data-id', element.id);

        btn.id = element.id;
        btn.className = "btn btn-sm " + botoes[nomeBotao].classe;
        btn.innerHTML = botoes[nomeBotao].texto;
  
        if (botoes[nomeBotao].callback) {
          // Use uma função anônima para passar o ID
          btn.onclick = function() {
            // Chame a função de callback passando o ID
            botoes[nomeBotao].callback(element.id);
          };
        }
        tdBotao.appendChild(btn);
        tr.appendChild(tdBotao);
      }
    }
    tbody.appendChild(tr);
  });
};

  
  
/**
 * Limpa o conteúdo de um corpo de tabela, removendo todas as linhas.
 * @param {string} id_tbody - O ID do corpo da tabela a ser limpo.
 * @example
 * // Exemplo de chamada da função para limpar o corpo de uma tabela com ID 'tabelaCorpo'
 * limpa_tabelas('tabelaCorpo');
 */
const limpa_tabelas = (id_tbody) => {
  /**
   * Limpa o conteúdo de um corpo de tabela, removendo todas as linhas.
   * @function
   * @param {string} id_tbody - O ID do corpo da tabela a ser limpo.
   */
  const tbody = document.getElementById(id_tbody);
  tbody.innerHTML = "";
};

  
