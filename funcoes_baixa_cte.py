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
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.keys import Keys
import zipfile
import requests
from datetime import datetime
from shutil import rmtree
import shutil

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

def _criar_pasta_se_nao_existir(caminho):
    """Cria uma pasta se ela não existir."""
    if not os.path.exists(caminho):
        os.makedirs(caminho)
        print(f"Pasta {caminho} criada.")

def _criar_pasta_temporaria():
    """Cria uma pasta temporária para armazenar os PDFs."""
    hoje = datetime.now().strftime('%Y-%m-%d')
    pasta_temporaria = os.path.join(os.getcwd(), 'downloads_temp', hoje)
    _criar_pasta_se_nao_existir(pasta_temporaria)
    return pasta_temporaria

def _realizar_login(driver, usuario, senha):
    """Realiza o login no sistema."""
    driver.get("https://lonngren.app")
    driver.find_element(By.ID, "usuario").send_keys(usuario)
    driver.find_element(By.ID, "senha").send_keys(senha)
    driver.find_element(By.ID, "acesso").click()
    WebDriverWait(driver, 10).until(EC.url_contains("https://lonngren.app/techno/"))
    print("Login realizado com sucesso.")

def _acessar_pagina(driver, url):
    """Acessa uma página específica."""
    driver.get(url)

def _selecionar_dropdown(driver):
    # Espera até que o botão do dropdown esteja clicável e clica nele para abrir
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class='btn btn-primary dropdown-toggle ng-binding']"))
    )
    dropdown_button.click()

    # Espera até o item "CTe/Minuta" estar clicável dentro do dropdown e clica nele
    cte_minuta_item = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'CTe/Minuta')]"))
    )
    cte_minuta_item.click()

def _pesquisa_cte(driver,array_ctes):

    for cte in array_ctes:

        _acessar_pagina(driver, "https://lonngren.app/mobile/")

        _selecionar_dropdown(driver)
        
        print(f'Trabalhando no cte {cte}')
        # Espera o campo de pesquisa ficar visível e preenche-o com o valor desejado
        campo_pesquisa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='search']"))
        )
        campo_pesquisa.send_keys(cte)  # Substitua pelo número do documento

        # Clica no botão de pesquisa para submeter
        botao_pesquisa = driver.find_element(By.XPATH, "//button[@type='submit']")
        botao_pesquisa.click()        

        # Aguardar o carregamento ou o término da busca, se necessário
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//span[@ng-show='spinBuscando']"))
        )

        # Espera até que o primeiro link da tabela esteja clicável e clica nele
        primeiro_pedido_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//td[.//a[@ng-click='buscaPedido(ctrc.pedido)']]//a"))
        )
        primeiro_pedido_link.click()

        # Espera até que o botão do dropdown DACTE esteja visível e interativo (não sobreposto)
        dropdown_button_cte = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@id='dacteDropdown']"))
        )

        driver.execute_script("arguments[0].click();", dropdown_button_cte)

        # Agora, podemos clicar em "1 por página"
        um_por_pagina_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '1 por pagina')]"))
        )
        um_por_pagina_item.click()

def ctes_lote(usuario, senha,array_ctes):
    """Fluxo principal para realizar o web scraping de coletas em lote."""
    download_dir = _criar_pasta_temporaria()
    driver = _configurar_driver(download_dir)

    # try:
    _realizar_login(driver, usuario, senha)

    _pesquisa_cte(driver, array_ctes)

    time.sleep(1)

    driver.quit()

    return processar_download_pdfs(download_dir)

