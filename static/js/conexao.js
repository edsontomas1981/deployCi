const BASEURL = "http://54.91.211.206/";

class ApiService {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }

    async getAll(endpoint) {
        const response = await fetch(`${this.baseUrl}/${endpoint}`);
        return this.handleResponse(response);
    }

    async getById(endpoint, id) {
        const response = await fetch(`${this.baseUrl}/${endpoint}/${id}`);
        return this.handleResponse(response);
    }

    async create(endpoint, data) {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    async post(endpoint, data) {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    async update(endpoint, id, data) {
        const response = await fetch(`${this.baseUrl}/${endpoint}/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return this.handleResponse(response);
    }

    async delete(endpoint, id) {
        const response = await fetch(`${this.baseUrl}/${endpoint}/${id}`, {
            method: 'DELETE', // Corrigido para usar DELETE
            headers: {
                'Content-Type': 'application/json' // Opcional para DELETE, mas mantém consistência
            }
        });
        return this.handleResponse(response);
    }

    /**
   * Método para buscar registros com filtros flexíveis.
   * @param {string} endpoint - O endpoint da API.
   * @param {Object} filters - Filtros para a busca.
   * @returns {Promise<Object>} - Resultado da busca.
   */
    async search(endpoint, filters) {
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(filters)
        });
        return this.handleResponse(response);
    }

    async handleResponse(response) {
        // Verifica se o conteúdo é um blob (arquivo)
        const contentType = response.headers.get("Content-Type");
        if (contentType && contentType.includes("application/zip")) {
            return response.blob();  // Retorna o arquivo como blob
        }

        // Caso contrário, retorna como JSON
        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }
        return response.json();
    }

    /**
     * Faz o download de um arquivo após um POST com dados.
     * @param {string} endpoint - O endpoint para o qual o POST será feito.
     * @param {Object} data - Dados que serão enviados no corpo do POST.
     */
    async downloadFile(endpoint, data) {
        // Fazendo o POST com os dados
        const response = await fetch(`${this.baseUrl}/${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)  // Dados enviados no POST
        });

        // Obtém o arquivo como um Blob
        const blob = await this.handleResponse(response);

        // Cria um link para o download do arquivo
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'download.zip';  // Nome do arquivo que será baixado
        document.body.appendChild(a);
        a.click();  // Dispara o download
        a.remove();  // Remove o link da página
    }
}

const formataDataPtBr = (dataString)=>{
  
    const dataObj = new Date(dataString);
    // Usando 'pt-BR' para obter o formato brasileiro
    const formatoBrasileiro = new Intl.DateTimeFormat('pt-BR', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
    });
  
    return formatoBrasileiro.format(dataObj);
}


class Conn {
    constructor(url, data) {
        this.url = BASEURL + url;
        this.data = data;
    }

    getCSRFToken = async () => {
        try {
            const response = await fetch(BASEURL+'/produtos/api/get_csrf_token/', {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data.csrf_token;
        } catch (error) {
            console.error(error);
            return null;
        }
    };
    

    async sendPostRequest(url, data) {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function transformarEmListaDeListas(data) {
    // Criar uma lista vazia para armazenar as listas de objetos
    const listaDeListas = [];
  
    // Iterar sobre cada objeto na lista de dados
    for (const objeto of data) {
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
  

function formatarData(dataString) {
    const partesData = dataString.split('-');
    const dia = partesData[0];
    const mes = partesData[1];
    const ano = partesData[2];
    return `${dia}-${mes}-${ano}`;
}
