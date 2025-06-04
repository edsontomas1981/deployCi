#!/bin/bash

# Caminho para o diretório do projeto
PROJECT_DIR="/home/edson/Documentos/deployNorte"

# Navegue até o diretório do projeto
cd "$PROJECT_DIR" || exit

# Ative o ambiente virtual
source vnv/bin/activate

# Inclua o diretório raiz no PYTHONPATH
export PYTHONPATH=$PROJECT_DIR

# Variáveis de ambiente do Flask
export FLASK_APP=app.py
export FLASK_ENV=development

# Inicia o servidor Flask
flask run --host=0.0.0.0 --port=5000

# Pausa para visualizar mensagens
echo "Pressione qualquer tecla para sair..."
read -n1 -s
