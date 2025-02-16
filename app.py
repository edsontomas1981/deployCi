from flask import Flask, request, jsonify,send_file, render_template
from flask_cors import CORS
import sqlite3
import json
from impressao_ci import imprimir_ci
from iscas import localiza_iscas
from funcoes_pega_coleta import webscrap_coletas,webscrap_coletas_lote,download_coletas
from funcoes_baixa_cte import ctes_lote,processar_download_pdfs
from flask_socketio import SocketIO, send, emit, join_room
from flask import send_from_directory
import os
import shutil
import zipfile
import requests
import json

from contatos import create_contato,get_contato_by_fone,update_contato_nome
from estados_contatos import get_estado_contato_by_telefone,create_estado_contato,update_estado_contato
from cadastro_contatos import cadastrar_contatos
from menu import gerar_menu,selecao_menu
from messages import create_mensagem
from coletas import carrega_dados_coleta
from utils import busca_cep_ws
from carrega_coordenadas import carrega_coordenadas


app = Flask(__name__, template_folder='templates', static_folder='static')

# Permitir CORS para qualquer origem
# CORS(app, resources={r"/*": {"origins": "*"}})

socketio = SocketIO(app, cors_allowed_origins="*")  # Permitir conexões de qualquer origem


DATABASE = 'bd_norte.db'

@socketio.on("message")
def handle_mensagens (data):
    telefone = data.get("phone")
    mensagem = data.get("msg")
    nome = data.get('nome')

    estado_contato = get_estado_contato_by_telefone(telefone)

    if not estado_contato:
        try:
            create_contato(telefone)
            create_estado_contato((telefone, 0,mensagem,1 ))
            create_mensagem(telefone,mensagem)   
            send("Olá! Percebi que ainda não sei o seu nome.  Para que possamos atendê-lo melhor, você poderia me informar o seu nome, por favor?")
        except:
            send("Ops, ocorreu um erro! Por favor, tente novamente mais tarde. 😊")
        return
    
    create_mensagem(telefone,mensagem)                    
    contato = get_contato_by_fone(telefone)

    match str(estado_contato[1]):
        case "0":
            match str(estado_contato[4]):
                case '1':   
                    update_estado_contato(telefone, 1, 1, mensagem)
                    update_contato_nome(telefone, mensagem)
                    contato = get_contato_by_fone(telefone)
                    send(f'Olá, {contato[3]}! Tudo bem? Vou te mostrar o nosso menu de opções. 😊 {gerar_menu()}')
                    return  

        case "1":
            match str(estado_contato[4]):
                case '1': # Selecione a opcao
                    send(selecao_menu(estado_contato,mensagem,telefone))                

        case "2":
            estado_contato = get_estado_contato_by_telefone(telefone)
            json_atual = (json.loads(estado_contato[2]))
            temp_json = carrega_dados_coleta(json_atual,mensagem)
            
            if temp_json:
                json_atual = temp_json
           
            update_estado_contato(telefone, 2, 0,json.dumps(json_atual))
            send(json_atual.get('pergunta'))
   

    return jsonify({"resposta": 'resposta'})

def enviar_mensagem_para_cliente():
    url = "https://graph.facebook.com/v21.0/559569933902545/messages"

    access_token = "EAANxmkzeEj8BO85QJsrCGXqWebvoJZBu3g27YraLQyltLNeOehOjFLoU0Cvp89aHYLMJLoZCZATD3o19u90QHd2oR1QYNNhQUwgZBmi7haKZBcN49UEQVGitJHDInZBTZCs6vR5xeYQ6FaqCne5MlMotFKQyz5tCaixsnlZCFuQSVzvPGApRo5fIgAPD6wVxCFMmLEnZBoBDLnn7zN4tYoLqWA9CZBJkQ4AdBC1WY2"

    data = {
            "messaging_product": "whatsapp",
            "to": "5511969262277",
            "type": "text",
            "text": {
                "body": "teste via python"
            }
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
        send('sua mensagem foi enviada')
    else:
        print(f"Erro ao enviar a mensagem: {response.status_code}")
        print(response.text)

# Rota principal para carregar a interface do chat
@app.route('/chat')
def chat():
    # enviar_mensagem_para_cliente()
    status_code,json_endereco = busca_cep_ws('07243180')
    print(f"Coordenadas : {json_endereco.get('location').get('coordinates')}")
    return render_template('chat.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/main_carregamento', methods=['GET'])
def main_carregamento():
    return render_template('main_carregamento.html')

@app.route('/carregamentos', methods=['GET'])
def carregamento():
    return render_template('carregamento.html')

@app.route('/entrada_notas', methods=['GET'])
def entradaNfs():
    return render_template('entradaNotas.html')

@app.route('/novoInicio', methods=['GET'])
def newIndex():
    return render_template('novo.html')

@app.route('/template', methods=['GET'])
def template():
    return render_template('template.html')

@app.route('/envio_coletas', methods=['GET'])
def envio_coletas():
    return render_template('downloadsColetas.html')

@app.route('/cidades_atendidas', methods=['GET'])
def cidades_atendidas():
    return render_template('relacaoCidadesAtendidas.html')

@app.route('/iscas', methods=['GET'])
def iscas():
    return render_template('relatorioIscas.html')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

@app.route('/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    return response

@app.route('/report_iscas', methods=['GET', 'POST'])
def report_iscas():
    relat_iscas = localiza_iscas()
    return jsonify(relat_iscas)

@app.route('/comunicacoes', methods=['GET'])
def get_comunicacoes():
    conn = get_db_connection()
    comunicacoes = conn.execute('SELECT * FROM comunicacao_interna ORDER BY ci_num DESC').fetchall()
    conn.close()
    return jsonify([dict(row) for row in comunicacoes])

@app.route('/print_comunicacao', methods=['POST'])
def print_comunicacao():
    data = request.get_json()
    if not data or 'ci_num' not in data:
        return jsonify({'error': 'ci_num is required'}), 400
    ci_num = data['ci_num']
    conn = get_db_connection()
    comunicacao = conn.execute('SELECT * FROM comunicacao_interna WHERE ci_num = ?', (ci_num,)).fetchone()
    conn.close()
    if comunicacao is None:
        return jsonify({'error': 'Comunicação não encontrada'}), 404
    imprimir_ci(dict(comunicacao))
    return jsonify(dict(comunicacao))

@app.route('/comunicacao/<int:ci_num>', methods=['GET'])
def get_comunicacao(ci_num):
    conn = get_db_connection()
    comunicacao = conn.execute('SELECT * FROM comunicacao_interna WHERE ci_num = ?', (ci_num,)).fetchone()
    conn.close()
    if comunicacao is None:
        return jsonify({'error': 'Comunicação não encontrada'}), 404
    return jsonify(dict(comunicacao))

@app.route('/comunicacao', methods=['POST'])
def create_comunicacao():
    data = request.get_json()
    destinatario = data.get('destinatario')
    manifesto_numero = data.get('manifesto_numero')
    motorista = data.get('motorista')
    valor_frete = data.get('valor_frete')
    percurso = data.get('percurso')
    data_comunicacao = data.get('data')
    observacao = data.get('observacao')
    isca_1 = data.get('isca_1')
    isca_2 = data.get('isca_2')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO comunicacao_interna
                      (destinatario, manifesto_numero, motorista, valor_frete, percurso, data, observacao, isca_1, isca_2)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (destinatario, manifesto_numero, motorista, valor_frete, percurso, data_comunicacao, observacao, isca_1, isca_2))

    comunicacao_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'status': 'Comunicação criada com sucesso'}), 201

@app.route('/get_coletas', methods=['POST'])
def get_coletas():
    numero_pedidos = request.get_json()
    USUARIO = 'edson@nor'
    SENHA = 'analu1710'
    webscrap_coletas(USUARIO,SENHA,numero_pedidos)
    return jsonify({'status': 'Comunicação criada com sucesso'}), 201

@app.route('/comunicacao/<int:ci_num>', methods=['PUT'])
def update_comunicacao(ci_num):
    data = request.get_json()
    destinatario = data['destinatario']
    manifesto_numero = data['manifesto_numero']
    motorista = data['motorista']
    valor_frete = data['valor_frete']
    percurso = data['percurso']
    data_comunicacao = data['data']
    observacao = data['observacao']
    isca_1 = data['isca_1']
    isca_2 = data['isca_2']

    conn = get_db_connection()
    conn.execute('UPDATE comunicacao_interna SET destinatario = ?, manifesto_numero = ?, motorista = ?, valor_frete = ?, percurso = ?, data = ?, observacao = ?, isca_1 = ?, isca_2 = ? WHERE ci_num = ?',
                 (destinatario, manifesto_numero, motorista, valor_frete, percurso, data_comunicacao, observacao, isca_1, isca_2, ci_num))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Comunicação atualizada com sucesso'})

@app.route('/comunicacao/<int:ci_num>', methods=['DELETE'])
def delete_comunicacao(ci_num):
    conn = get_db_connection()
    conn.execute('DELETE FROM comunicacao_interna WHERE ci_num = ?', (ci_num,))
    conn.commit()
    conn.close()
    return jsonify({'status': 'Comunicação deletada com sucesso'})

@app.route('/selecionar_ci', methods=['POST'])
def select_ci():
    """
    Realiza uma busca flexível na tabela 'comunicacao_interna' com base em filtros opcionais.

    Filtros opcionais:
    - 'percurso': Busca por trecho do percurso.
    - 'observacao': Busca por trecho da observação.
    - 'motorista': Busca por nome do motorista.
    - 'isca': Busca por valores em 'isca_1' ou 'isca_2'.

    Retorna:
    - Lista de registros encontrados em formato JSON ou mensagens de erro apropriadas.
    """
    data = request.get_json()

    data = data.get('dados')

    # Coleta os filtros enviados
    percurso = data.get('percurso')
    observacao = data.get('observacao')
    motorista = data.get('motorista')
    isca = data.get('isca')

    # Monta a query base
    query = "SELECT * FROM comunicacao_interna WHERE 1=1"
    params = []

    # Adiciona filtros opcionais, se fornecidos
    if percurso:
        query += " AND percurso LIKE ?"
        params.append(f"%{percurso}%")
    if observacao:
        query += " AND observacao LIKE ?"
        params.append(f"%{observacao}%")
    if motorista:
        query += " AND motorista LIKE ?"
        params.append(f"%{motorista}%")
    if isca:
        # Busca por 'isca' em 'isca_1' ou 'isca_2'
        query += " AND (isca_1 LIKE ? OR isca_2 LIKE ?)"
        params.append(f"%{isca}%")
        params.append(f"%{isca}%")

    # Ordena os resultados em ordem decrescente com base na coluna 'ci_num'
    query += " ORDER BY ci_num DESC"

    # Conexão e execução da consulta
    conn = get_db_connection()
    comunicacoes = conn.execute(query, params).fetchall()
    conn.close()

    # Verifica se encontrou registros
    if not comunicacoes:
        return jsonify({'error': 'Nenhuma comunicação encontrada'}), 404

    # Retorna os resultados como uma lista de dicionários
    resultados = [dict(comunicacao) for comunicacao in comunicacoes]
    return jsonify(resultados)

@app.route('/ctes', methods=['GET'])
def home_ctes():
    return render_template('baixarCtes.html')

@app.route('/baixar_coletas_lote', methods=['POST'])
def baixar_coletas_lote():
    numero_pedidos = request.get_json()
    USUARIO = 'edson@nor'
    SENHA = 'analu1710'
    zip_file,arquivos_sucesso,arquivos_erro = download_coletas(USUARIO,SENHA,numero_pedidos)

    # Criar um JSON contendo os status dos arquivos
    status_json = {
        "arquivos_sucesso": arquivos_sucesso,
        "arquivos_erro": arquivos_erro
    }

    # Enviar o ZIP no corpo da resposta e o JSON nos headers
    response = send_file(zip_file, as_attachment=True, download_name='coletas_lote.zip', mimetype='application/zip')
    response.headers['X-Status-Json'] = json.dumps(status_json)  # ✅ CORRETO
    return response

@app.route('/baixar_ctes_lote', methods=['POST'])
def baixar_ctes_lote():
    try:
        # Defina as credenciais
        USUARIO = 'edson@nor'
        SENHA = 'analu1710'

        # Obter o número dos CTEs (presumindo que seja enviado via JSON)
        numero_ctes = request.get_json()

        erros = [1,2,3]

        sucessos = [1,2,3]
        # Gerar o diretório de download
        zip_filename,arquivos_sucesso,arquivos_erro = ctes_lote(USUARIO, SENHA, numero_ctes)

        # Criar um JSON contendo os status dos arquivos
        status_json = {
            "arquivos_sucesso": arquivos_sucesso,
            "arquivos_erro": arquivos_erro
        }

        # Enviar o ZIP no corpo da resposta e o JSON nos headers
        response = send_file(zip_filename, as_attachment=True, download_name='coletas_lote.zip', mimetype='application/zip')
        response.headers['X-Status-Json'] = json.dumps(status_json)  # ✅ CORRETO
        return response

        # return send_file(zip_filename, as_attachment=True, download_name='ctes_lote.zip', mimetype='application/zip')

    except Exception as e:
        print(f"Erro ao baixar os CTEs: {e}")
        return jsonify({'status': 'Erro durante o processo'}), 500

# Rota para receber mensagens da API do WhatsApp
@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # Verifica se é uma requisição de verificação do webhook
    if request.method == 'GET':
        # Parâmetros fornecidos pelo WhatsApp
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        # Verifica se o token de verificação é válido
        VERIFY_TOKEN = "EAANxmkzeEj8BOZC5K3TNDIpuFG60P5CP008kyH7YZBBAsqWNro60pmKgNy4NfWHFfkEnNO760krXu73Fu8h6NW7O7j58h5A8m9mHTOt4yLOvXGgRDn1FHpFd2olIwEbbxHZBZBylS85D7dPrIuLCUtopDNPZCRiD4JwWNAAPiicZAIBbfHCpZArIjZBEeS3HfVSTHmc7wayopaNGZCJZBSp7nYLy0ZCfFCfZCSZAj7FAZD"  # Substitua pelo token configurado no WhatsApp
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verificado com sucesso!")
            return challenge, 200
        else:
            return "Token de verificação inválido", 403

    # Processa mensagens recebidas (POST)
    if request.method == 'POST':
        data = request.get_json()  # Obtém o JSON enviado pela API
        print("Mensagem recebida:", data)

        # Exemplo: Extrair informações da mensagem
        if 'entry' in data and len(data['entry']) > 0:
            for entry in data['entry']:
                for change in entry.get('changes', []):
                    if change['value']['messaging_product'] == 'whatsapp':
                        messages = change['value'].get('messages', [])
                        for message in messages:
                            phone_number = message['from']  # Número do remetente
                            message_text = message['text']['body']  # Conteúdo da mensagem
                            print(f"Mensagem de {phone_number}: {message_text}")

        return jsonify({"status": "success"}), 200
    
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)