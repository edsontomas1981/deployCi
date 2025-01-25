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

// Função que realiza a busca no JSON por trechos do nome da cidade, desconsiderando os acentos
function buscarCidade(json, cidadeBuscada) {
    // Normaliza a cidade buscada removendo os acentos
    const cidadeBuscadaNormalizada = cidadeBuscada.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    
    // Filtra o JSON pelas cidades que contêm o trecho buscado, desconsiderando os acentos
    const resultado = json.filter(item => 
      item.cidade.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().includes(cidadeBuscadaNormalizada)
    );
  
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
