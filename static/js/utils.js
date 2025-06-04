/**
 * Extrai palavras de um textarea, separando por espaços ou quebras de linha.
 * @param {string} textareaId - O ID do textarea de onde o texto será extraído.
 * @returns {string[]} - Um array de palavras separadas por espaços ou enter.
 */
function getWordsFromTextarea(textareaId) {
    // Obtém o valor do textarea
    const textarea = document.getElementById(textareaId);
    if (!textarea) {
        console.error("Textarea não encontrado!");
        return [];
    }

    const text = textarea.value;

    // Divide o texto em palavras, considerando espaços e enter como delimitadores
    const wordsArray = text.split(/\s+/).filter(word => word.trim() !== "");

    return wordsArray;
}

// Funções auxiliares
function updateProgressBar(value) {
    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = `${value}%`;
    progressBar.setAttribute('aria-valuenow', value);
}

function showLoader(message) {
    const loader = document.getElementById('loader');
    loader.classList.remove('d-none');
    mensagemDeCarga.textContent = message;
}

function hideLoader() {
    const loader = document.getElementById('loader');
    loader.classList.add('d-none');
}

// Função que ordena o JSON alfabeticamente pela chave 'cidade'
function ordenarPorCidade(json) {
    return json.sort((a, b) => a.cidade.localeCompare(b.cidade));
}

function buscarCidade(dados, cidadeBuscada) {
    // Normaliza a cidade buscada removendo os acentos
    const cidadeBuscadaNormalizada = cidadeBuscada
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .toLowerCase();

    // Filtra as listas onde a cidade (índice 1) contém o trecho buscado
    const resultado = dados.filter(item => {
        const cidade = item[1]; // cidade está no índice 1
        const cidadeNormalizada = cidade
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .toLowerCase();

        return cidadeNormalizada.includes(cidadeBuscadaNormalizada);
    });

    return resultado;
}


/**
 * Exibe uma mensagem de confirmação com dois botões (Confirmar e Cancelar)
 * e retorna uma Promise que resolve para `true` se o usuário confirmar,
 * ou `false` se o usuário cancelar.
 *
 * @param {string} msg - A mensagem que será exibida na caixa de diálogo.
 * @returns {Promise<boolean>} Uma Promise que resolve para `true` se o usuário clicar em "Confirmar",
 * ou `false` se o usuário clicar em "Cancelar".
 *
 * @example
 * // Exemplo de uso:
 * msgConfirmacao('Você tem certeza?').then((confirmado) => {
 *   if (confirmado) {
 *     console.log('Usuário confirmou.');
 *   } else {
 *     console.log('Usuário cancelou.');
 *   }
 * });
 */
const msgConfirmacao = async (msg) => {
    return new Promise(async (resolve) => {
      const result = await Swal.fire({
        title: msg,
        showDenyButton: true,
        confirmButtonText: "Confirmar",
        denyButtonText: "Cancelar",
      });

      if (result.isConfirmed) {
        resolve(true);
      } else {
        resolve(false);
      }
    });
  };

  const msgOk = (msg) => {
    Swal.fire({
      position: "top-end",
      icon: "success",
      title: msg,
      showConfirmButton: false,
      timer: 1500,
    });
  };

  const msgAlerta = (msg) => {
    Swal.fire(msg);
  };

  const msgInfo = (dadosMsg) => {
    Swal.fire({
      title: dadosMsg.titulo,
      text: dadosMsg.msg,
      icon: "info",
    });
  };

  const msgErro = (msg) => {
    Swal.fire({
      position: "top-end",
      icon: "error",
      title: msg,
      showConfirmButton: false,
      timer: 3000,
    });
  };

  const msgErroFixa = (msg) => {
    Swal.fire({
      title: "Erro !",
      text: msg,
      icon: "error",
    });
  };

  const msgAviso = (msg) => {
    Swal.fire({
      position: "top-end",
      icon: "warning",
      title: msg,
      showConfirmButton: false,
      timer: 3000,
    });
  };

  /**
 * Separa os componentes da chave de acesso de uma Nota Fiscal Eletrônica (NF-e).
 *
 * A chave de acesso é composta por 44 dígitos numéricos com a seguinte estrutura:
 * 1-2     - UF
 * 3-4     - Ano e Mês de emissão
 * 5-8     - CNPJ do emitente
 * 9-22    - Modelo, série e número da NF
 * 23-34   - Código numérico e dígito verificador
 * 35-43   - Tipo de emissão e data de emissão
 * 44      - Dígito verificador geral
 *
 * @param {string} chave - Chave de acesso completa da NF-e (44 caracteres numéricos)
 * @returns {Object} Objeto com os componentes separados da chave de acesso
 * @throws {Error} Se a chave não tiver exatamente 44 caracteres numéricos
 *
 * @example
 * const chave = '43171207364617000135550000000120141000120140';
 * const componentes = separarChaveNFe(chave);
 * console.log(componentes);
 * // Retorna:
 * // {
 * //   uf: '43',
 * //   anoMes: '17',
 * //   cnpj: '07364617000135',
 * //   modeloSerieNumero: '5500000001201',
 * //   codigoDV: '4100012014',
 * //   tipoEmissaoData: '0',
 * //   dvGeral: '0'
 * // }
 */
  function separarChaveNFe(chave) {
    if (typeof chave !== 'string' || chave.length !== 44 || !/^\d+$/.test(chave)) {
        throw new Error('Chave de acesso inválida. Deve conter exatamente 44 dígitos numéricos.');
    }

    return {
        uf: chave.substring(0, 2),
        anoMes: chave.substring(2, 4),
        cnpj: chave.substring(6, 20),
        modelo: chave.substring(20, 22), // Modelo da NF-e (2 dígitos)
        serie: chave.substring(22, 25),  // Série da NF-e (3 dígitos)
        numero: chave.substring(25, 34), // Número da NF-e (9 dígitos)
        codigoDV: chave.substring(34, 44),
        tipoEmissaoData: chave.substring(35, 43),
        dvGeral: chave.substring(43, 44)
    };
}



/**
 * Obtém a data e a hora atuais no formato brasileiro.
 *
 * @returns {Object} Um objeto contendo a data e a hora formatadas.
 * @property {string} data - Data atual no formato "DD/MM/AAAA".
 * @property {string} hora - Hora atual no formato "HH:MM:SS".
 *
 * @example
 * const resultado = obterDataHoraAtual();
 * console.log(`Data: ${resultado.data}, Hora: ${resultado.hora}`);
 */
function obterDataHoraAtual() {
  const agora = new Date();

  const data = agora.toLocaleDateString('pt-BR'); // Formato: DD/MM/AAAA
  const hora = agora.toLocaleTimeString('pt-BR'); // Formato: HH:MM:SS

  return { data, hora };
}

  function showLoaderSweet(msg) {
    Swal.fire({
        title: msg,
        allowOutsideClick: false,
        showConfirmButton: false,
        willOpen: () => {
            Swal.showLoading();
        }
    });
}


function hideLoaderSweet() {
    Swal.close();
}

/**
 * Popula um select box HTML com opções fornecidas.
 *
 * @param {string} idSelect - O ID do elemento select.
 * @param {Array} value - Array de objetos com as propriedades 'value' e 'text'.
 */
const populaSelect = (idSelect, value) => {
  const select = document.getElementById(idSelect);
  if (!select) {
    console.warn(`Elemento com ID "${idSelect}" não encontrado.`);
    return;
  }

  // Limpa as opções existentes
  select.innerHTML = '';

  // Cria e adiciona as novas opções
  value.forEach(item => {
    const option = document.createElement('option');
    option.value = item.value;
    option.text = item.text;
    select.appendChild(option);
  });
};

/**
 * Seleciona um valor em um select box HTML, se estiver presente.
 *
 * @param {string} idSelect - O ID do elemento select.
 * @param {string} valor - O valor a ser selecionado.
 */
const selecionaValorSelect = (idSelect, valor) => {
  const select = document.getElementById(idSelect);
  if (!select) {
    console.warn(`Elemento com ID "${idSelect}" não encontrado.`);
    return;
  }

  const optionExiste = Array.from(select.options).some(opt => opt.value === valor);
  if (optionExiste) {
    select.value = valor;
  } else {
    console.warn(`Valor "${valor}" não encontrado no select "${idSelect}".`);
  }
};

/**
 * Retorna o value e o texto da opção selecionada em um select box.
 *
 * @param {string} idSelect - O ID do elemento select.
 * @returns {{ value: string, text: string } | null} - Objeto com value e text, ou null se não encontrado.
 */
const obterOpcaoSelecionada = (idSelect) => {
  const select = document.getElementById(idSelect);
  if (!select) {
    console.warn(`Elemento com ID "${idSelect}" não encontrado.`);
    return null;
  }

  const selectedOption = select.options[select.selectedIndex];
  if (!selectedOption) return null;

  return {
    value: selectedOption.value,
    text: selectedOption.text
  };
};
