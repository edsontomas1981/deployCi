import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import zipfile
import requests
from datetime import datetime
from shutil import rmtree
import shutil


def criar_pasta_temporaria():
    """Cria uma pasta temporária para armazenar os PDFs."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    pasta_temporaria = os.path.join(os.getcwd(), 'downloads_temp', hoje)
    criar_pasta_se_nao_existir(pasta_temporaria)
    return pasta_temporaria

def fazer_download_pdf(url, destino):
    """Faz o download do PDF e salva no destino especificado."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with open(destino, 'wb') as f:
            f.write(response.content)
        print(f"PDF {url} baixado com sucesso.")
    except Exception as e:
        print(f"Erro ao baixar o arquivo {url}: {e}")

def compactar_pasta_para_zip(pasta_temporaria):
    """Compacta a pasta temporária em um arquivo ZIP."""
    zip_file = f"{pasta_temporaria}.zip"
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(pasta_temporaria):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), pasta_temporaria))
    print(f"Pasta {pasta_temporaria} compactada em {zip_file}")
    return zip_file

def excluir_pasta_temporaria(pasta_temporaria):
    """Exclui a pasta temporária após o uso."""
    try:
        rmtree(pasta_temporaria)
        print(f"Pasta temporária {pasta_temporaria} excluída.")
    except Exception as e:
        print(f"Erro ao excluir a pasta temporária {pasta_temporaria}: {e}")

def obter_diretorio_download():
    """Obtém o diretório de download com base na data de hoje."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    download_dir = os.path.join(os.getcwd(), hoje)
    criar_pasta_se_nao_existir(download_dir)
    return download_dir

def criar_pasta_se_nao_existir(caminho):
    """Cria uma pasta se ela não existir."""
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"Pasta {caminho} criada.")

def obter_arquivos_pdf(pasta):
    """
    Obtém a lista de arquivos PDF de uma pasta local.
    
    Args:
        pasta (str): Caminho da pasta onde os PDFs estão armazenados.
        
    Returns:
        list: Lista de caminhos de arquivos PDF.
    """
    arquivos_pdf = []
    for filename in os.listdir(pasta):
        if filename.endswith(".pdf"):
            arquivos_pdf.append(os.path.join(pasta, filename))
    return arquivos_pdf

def compactar_pasta_para_zip(pasta_temporaria):
    """Compacta a pasta temporária em um arquivo ZIP."""
    zip_file = f"{pasta_temporaria}.zip"
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(pasta_temporaria):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), pasta_temporaria))
    print(f"Pasta {pasta_temporaria} compactada em {zip_file}")
    return zip_file

def _criar_pasta_temporaria():
    """Cria uma pasta temporária para armazenar os PDFs."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    pasta_temporaria = os.path.join(os.getcwd(), 'downloads_temp', hoje)
    _criar_pasta_se_nao_existir(pasta_temporaria)
    return pasta_temporaria

def _obter_arquivos_pdf(pasta):
    """
    Obtém a lista de arquivos PDF de uma pasta local.
    
    Args:
        pasta (str): Caminho da pasta onde os PDFs estão armazenados.
        
    Returns:
        list: Lista de caminhos de arquivos PDF.
    """
    arquivos_pdf = []
    for filename in os.listdir(pasta):
        if filename.endswith(".pdf"):
            arquivos_pdf.append(os.path.join(pasta, filename))

    print (f'Arq : {arquivos_pdf}')
    return arquivos_pdf

def _compactar_pasta_para_zip(pasta_temporaria):
    """Compacta a pasta temporária em um arquivo ZIP."""
    zip_file = f"{pasta_temporaria}.zip"
    
    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(pasta_temporaria):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), pasta_temporaria))
    print(f"Pasta {pasta_temporaria} compactada em {zip_file}")
    return zip_file

def _excluir_pasta_temporaria(pasta_temporaria):
    """Exclui a pasta temporária após o uso."""
    try:
        rmtree(pasta_temporaria)
        print(f"Pasta temporária {pasta_temporaria} excluída.")
    except Exception as e:
        print(f"Erro ao excluir a pasta temporária {pasta_temporaria}: {e}")

def _criar_pasta_se_nao_existir(caminho):
    """Cria uma pasta se ela não existir."""
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"Pasta {caminho} criada.")


def processar_download_pdfs(pasta):
    """
    Processa os PDFs de uma pasta, compacta e gera um arquivo ZIP para o download.
    
    Args:
        pasta (str): Caminho da pasta onde os PDFs estão localizados.
        
    Returns:
        str: Caminho do arquivo ZIP gerado.
    """
    pasta_temporaria = _criar_pasta_temporaria()

    # Copiar os arquivos PDF para a pasta temporária
    arquivos_pdf = _obter_arquivos_pdf(pasta)
    for arquivo_pdf in arquivos_pdf:
        destino = os.path.join(pasta_temporaria, os.path.basename(arquivo_pdf))
        
        # Verificar se o arquivo de origem e o destino são os mesmos
        if os.path.abspath(arquivo_pdf) != os.path.abspath(destino):
            shutil.copy(arquivo_pdf, pasta_temporaria)
        else:
            print(f"Arquivo {arquivo_pdf} já está presente em {destino}, ignorando cópia.")
    
    # Compactar a pasta
    zip_file = _compactar_pasta_para_zip(pasta_temporaria)
    
    # Excluir a pasta temporária
    _excluir_pasta_temporaria(pasta_temporaria)
    
    return zip_file
  
    # except Exception as e:
    #     print(f"Erro durante o processo: {e}")
    # finally:
    #     driver.quit()


    """Configura o WebDriver com as opções necessárias."""
    options = Options()
    # options.add_argument("--headless")  # Executa em modo headless
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def _realizar_login(driver, usuario, senha):
    """Realiza o login no sistema."""
    driver.get("https://lonngren.app")
    driver.find_element(By.ID, "usuario").send_keys(usuario)
    driver.find_element(By.ID, "senha").send_keys(senha)
    driver.find_element(By.ID, "acesso").click()
    WebDriverWait(driver, 10).until(EC.url_contains("https://lonngren.app/techno/"))
    print("Login realizado com sucesso.")

def realizar_login(driver, usuario, senha):
    """Realiza o login no sistema."""
    driver.get("https://lonngren.app")
    driver.find_element(By.ID, "usuario").send_keys(usuario)
    driver.find_element(By.ID, "senha").send_keys(senha)
    driver.find_element(By.ID, "acesso").click()
    WebDriverWait(driver, 10).until(EC.url_contains("https://lonngren.app/techno/"))
    print("Login realizado com sucesso.")

def acessar_pagina(driver, url):
    """Acessa uma página específica."""
    driver.get(url)

def buscar_pedido(driver, pedido):
    """Busca o pedido na página."""
    nroped_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pedido"))
    )
    nroped_input.send_keys(pedido)

    buscar_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "buscar"))
    )
    buscar_button.click()
    print(f"Pedido {pedido} buscado com sucesso.")
 
def clicar_aba_coleta(driver):
    """Clica na aba de coleta."""
    coleta_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="#tab-coleta"]'))
    )
    coleta_tab.click()
    print("Aba de coleta acessada.")

def imprimir_coleta(driver):
    """Clica no link para imprimir a coleta."""
    imprimir_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Imprimir Coleta"))
    )
    imprimir_link.click()
    print("Iniciada a impressão da coleta.")

def aguardar_download(download_dir, nome_arquivo):
    """Aguarda até que o arquivo seja baixado."""
    # pdf_file = os.path.join(download_dir, nome_arquivo)
    time.sleep(1)
    print(f"PDF baixado em: {nome_arquivo}")

def configurar_driver(download_dir):
    """Configura o WebDriver com as opções necessárias."""
    options = Options()
    options.add_argument("--headless")  # Executa em modo headless
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def _configurar_driver(download_dir):
    """Configura o WebDriver com as opções necessárias."""
    options = Options()
    options.add_argument("--headless")  # Executa em modo headless
    options.add_argument("--start-maximized")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def webscrap_coletas_lote(usuario, senha,array_coletas):
    """Fluxo principal para realizar o web scraping de coletas em lote."""
    download_dir = obter_diretorio_download()
    driver = configurar_driver(download_dir)

    try:
        realizar_login(driver, usuario, senha)
        for coleta in array_coletas:
            print(f'Trabalhando na coleta de numero {coleta}')
            acessar_pagina(driver, "https://lonngren.app/techno/sac/pedidos.php")
            buscar_pedido(driver, coleta)
            clicar_aba_coleta(driver)
            imprimir_coleta(driver)
            aguardar_download(download_dir, f'{coleta}')
        driver.quit()
    
        return download_dir
    
    except Exception as e:
        print(f"Erro durante o processo: {e}")
    finally:
        driver.quit()

def _pesquisa_coletas(driver,array_coletas,download_dir):
    for coleta in array_coletas:
        print(f'Trabalhando na coleta de numero {coleta}')
        acessar_pagina(driver, "https://lonngren.app/techno/sac/pedidos.php")
        buscar_pedido(driver, coleta)
        clicar_aba_coleta(driver)
        imprimir_coleta(driver)
        aguardar_download(download_dir, f'{coleta}')
    driver.quit()

def download_coletas(usuario, senha,array_coletas):
    """Fluxo principal para realizar o web scraping de coletas em lote."""
    download_dir = _criar_pasta_temporaria()
    driver = _configurar_driver(download_dir)

    # try:
    _realizar_login(driver, usuario, senha)

    _pesquisa_coletas(driver, array_coletas,download_dir)

    time.sleep(1)

    driver.quit()

    return processar_download_pdfs(download_dir)

def webscrap_coletas(usuario, senha, pedido):
    """Fluxo principal para realizar o web scraping de coletas."""
    download_dir = obter_diretorio_download()
    driver = configurar_driver(download_dir)

    try:
        realizar_login(driver, usuario, senha)
        acessar_pagina(driver, "https://lonngren.app/techno/sac/pedidos.php")
        buscar_pedido(driver, pedido)
        clicar_aba_coleta(driver)
        imprimir_coleta(driver)
        aguardar_download(download_dir, f'{pedido}')
        driver.quit()
        # return download_dir

        # Compacta os PDFs baixados
        zip_file = processar_download_pdfs(download_dir)
        print(f"Arquivo ZIP gerado: {zip_file}")
        return zip_file
    
    except Exception as e:
        print(f"Erro durante o processo: {e}")
    finally:
        driver.quit()
