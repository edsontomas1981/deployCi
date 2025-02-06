# Identifica campos enviados se estao vazios ou nao
# sendo identificacaoCampo e o nome vindo da requisição
# e nome campo e uma frase mais agradavel para retorno da requisição
from datetime import datetime, date
import re
import json
import math
from bradocs4py import CPF ,Cnpj
import requests

def checaCampos(request, **kwargs):
    camposVazios = []
    for identificacaoCampo, nomeCampo in kwargs.items():
        if request.POST.get(identificacaoCampo) == '':
            camposVazios.append(nomeCampo)
    return camposVazios

def checaCamposJson(json,**kwargs):
    # deve ser enviados kwargs com chaves e valores identificando quais 
    # campos sao obrigatorios e quais o nomes para apresenta-los ao usuario 
    # ex nomeContato="Nome do contato"
    listaDeCamposVazios = [nome_apresenta for campo, nome_apresenta in kwargs.items() if json.get(campo) == '']
    return listaDeCamposVazios
    
def checaCamposGeral(request, **kwargs):
    camposInvalidos = []
    for nomeCampo, value in kwargs.items():
        if testaCampos(request[nomeCampo][0], nomeCampo,regrasValidacao={nomeCampo: value}):
            camposInvalidos.append(nomeCampo)
    return camposInvalidos

def testaCampos(dado, tipo_dado):
    if isinstance(dado, tipo_dado):
        if tipo_dado == str:
            if not dado.strip():
                return "Campo não pode ser vazio"
        elif tipo_dado == int or tipo_dado == float:
            if dado <= 0:
                return "Valor não pode ser negativo ou zero"
        return True
    else:
        return "Tipo de dado inválido"

def verificaCamposObrigatorios(request):
    camposObrigatorios = []
    if request.POST.get('tipoTabela'):
        camposObrigatorios.append('Tipo da Tabela')
    if request.POST.get('freteMinimo'):
        camposObrigatorios.append('Frete mínimo')
    if request.POST.get('descTabela'):
        camposObrigatorios.append('Descrição da tabela')
    if request.POST.get('vlrFrete'):
        camposObrigatorios.append('Valor do Frete')
    if request.POST.get('tipoFrete'):
        camposObrigatorios.append('Tipo do frete')
    return camposObrigatorios

def toFloat(stringToFloat):
    if isinstance(stringToFloat,str ):
        if ',' in list(stringToFloat):
            stringToFloat = stringToFloat.replace(".", "")
            stringToFloat = stringToFloat.replace(",", ".")
            stringToFloat = float(stringToFloat)
    if stringToFloat:
        return float(stringToFloat)
    else:
        return 0
    
def to_float(value):
    """
    Converte uma string numérica em um float, lidando com formatos como "10.50", "10,50", "10.000,00".

    Parâmetros:
    ----------
    value : str, int, float
        O valor numérico a ser convertido.

    Retorna:
    -------
    float
        O valor convertido em float ou 0 se não for válido.
    """
    # Se o valor não for uma string, converta para string
    if not isinstance(value, str):
        value = str(value)

    # Se for uma string
    if isinstance(value, str):
        # Verifica se contém vírgula
        if ',' in value:
            # Remove separadores de milhar
            value = value.replace(".", "")
            value = value.replace(",", ".")

        # Tenta converter para float
        try:
            return float(value)
        except ValueError:
            return 0  # Retorna 0 se a conversão falhar

    return 0  # Retorna 0 se o valor não for uma string ou número

def checkBox(check):
    if check == 'on' or check == 1:
        return True
    elif check:
        return False
    else:
        return False

def checaUf(uf):
    listaUf = ['RO', 'AC', 'AM', 'RR', 'PA', 'AP', 'TO',
               'MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL',
               'SE', 'BA', 'MG', 'ES', 'RJ', 'SP', 'PR',
               'SC', 'RS', 'MS', 'MT', 'GO', 'DF']
    if uf in listaUf:
        return True
    else:
        return False

def remove_caracteres_cep(cep):
    """Remove caracteres especiais de um CEP e retorna apenas os dígitos."""
    return re.sub(r'\D', '', cep)

def remove_caracteres_cnpj_cpf(cnpj_cpf):
    """Remove caracteres especiais de um CNPJ/CPF e retorna apenas os dígitos."""
    return re.sub(r'\D', '', cnpj_cpf)

def string_para_data(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        return data
    except ValueError:
        print("Formato de data inválido. Utilize o formato 'YYYY-MM-DD'.")

def converte_string_data(data_str):
    formatos = ['%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y', '%Y/%m/%d', '%m/%d/%Y', '%d/%m/%Y', '%y/%m/%d']

    if isinstance(data_str, datetime.date):
        return data_str  # Se já for um datetime.date, retorne como está

    for formato in formatos:
        try:
            data = datetime.strptime(data_str, formato).date()
            return data
        except ValueError:
            continue
    print("Formato de data inválido. Utilize um dos formatos suportados: 'YYYY-MM-DD', 'DD-MM-YYYY', 'MM-DD-YYYY', 'YYYY/MM/DD', 'MM/DD/YYYY', 'DD/MM/YYYY', 'YY/MM/DD'.")
    return None

def str_to_date(data_str):
    """
    Converte uma string representando uma data em um objeto datetime.
    
    Tenta vários formatos de data e hora. Se a conversão falhar, retorna None.
    
    Args:
        data_str (str): A string a ser convertida para datetime.
        
    Returns:
        datetime: O objeto datetime correspondente ou None se a conversão falhar.
    """

    # Verifica se data_str é None ou uma string vazia
    if not data_str:
        return None 
    
    formatos = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%Y.%m.%d",
        "%d.%m.%Y",
        "%d %b %Y",
        "%d %B %Y",
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y %H:%M",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%d.%m.%Y %H:%M:%S",
        "%d.%m.%Y %H:%M",
        "%d %b %Y %H:%M:%S",
        "%d %b %Y %H:%M",
        "%d %B %Y %H:%M:%S",
        "%d %B %Y %H:%M"
    ]
    
    for formato in formatos:
        try:
            return datetime.strptime(data_str, formato)
        except ValueError:
            continue
    
    return None

def string_para_data(data_str):
    # Verifica se já é um objeto do tipo date
    if isinstance(data_str, date):
        return data_str

    # Verifica se é uma string válida e converte para data
    if isinstance(data_str, str) and data_str != '':
        data_str = datetime.strptime(data_str, "%Y-%m-%d").date()
        return data_str

    # Retorna None se a entrada for inválida
    return None

def calculo_distancia_coordenadas_haversine(ponto_inicial_lat, ponto_inicial_lng, destino_lat, destino_lng):
    # Raio médio da Terra em quilômetros
    R = 6371

    # Convertendo para radianos
    ponto_inicial_lat = math.radians(ponto_inicial_lat)
    ponto_inicial_lng = math.radians(ponto_inicial_lng)
    destino_lat = math.radians(destino_lat)
    lon2 = math.radians(destino_lng)

    # Fórmula de Haversine
    dlat = destino_lat - ponto_inicial_lat
    dlon = lon2 - ponto_inicial_lng
    a = math.sin(dlat/2)**2 + math.cos(ponto_inicial_lat) * math.cos(destino_lat) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)) 
    distance = R * c

    return distance

def imprimirJsonTerminal(response):
    """
    Imprime o conteúdo de uma resposta JSON de maneira formatada no terminal.

    Parâmetros:
    - response: objeto de resposta (normalmente de requests) que contém JSON

    Exemplo de uso:
        response = requests.get('sua_url_aqui')
        imprimirJsonTerminal(response)
    """
    try:
        # Obtem o JSON da resposta e imprime formatado
        print(json.dumps(response.json(), indent=4, ensure_ascii=False))
    except json.JSONDecodeError:
        print("Erro: A resposta não contém um JSON válido.")

def pode_ser_inteiro(dado):
    """
    Verifica se um dado pode ser convertido para um inteiro.

    Args:
        dado (any): O dado a ser verificado.

    Returns:
        bool: True se pode ser convertido para inteiro, False caso contrário.
    """
    try:
        int(dado)
        return True
    except (ValueError, TypeError):
        return False

def documento_e_valido(documento):
    """
    Verifica se um documento (CPF ou CNPJ) é válido.

    Args:
        documento (str): O documento a ser verificado.

    Returns:
        bool: True se o documento for válido, False caso contrário.
    """
    documento = remove_caracteres_cnpj_cpf(documento)

    if len(documento) == 11:
        return CPF(documento).isValid
    elif len(documento) == 14:
        return Cnpj(documento).isValid
    else:
        return False

def busca_cnpj_ws(documento):
    try:
        url = f"https://receitaws.com.br/v1/cnpj/{documento}"

        headers = {"Accept": "application/json"}

        response = requests.get(url, headers=headers)

        return response.status_code, response.json()    
    except:
        return None,None