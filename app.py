from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from dotenv import load_dotenv

# Carrega as senhas do arquivo .env
load_dotenv()

app = Flask(__name__)
# A chave secreta é necessária para manter o usuário logado
app.secret_key = os.getenv('CHAVE_SECRETA', 'chave_padrao_de_emergencia') 

ARQUIVO_DADOS = 'dados.json'

# --- SISTEMA DE LOGIN (A Mágica da Proteção) ---

# Essa função roda ANTES de qualquer requisição no site
@app.before_request
def verificar_login():
    # Se o usuário não estiver logado e tentar acessar qualquer coisa que não seja a tela de login ou os arquivos CSS/JS, ele é chutado pro login.
    if request.endpoint not in ['login', 'static'] and 'logado' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario_digitado = request.form.get('usuario')
        senha_digitada = request.form.get('senha')
        
        # Puxa o usuário e senha lá do arquivo .env
        usuario_correto = os.getenv('MEU_USUARIO')
        senha_correta = os.getenv('MINHA_SENHA')

        if usuario_digitado == usuario_correto and senha_digitada == senha_correta:
            session['logado'] = True # Salva que o usuário está logado
            return redirect(url_for('index'))
        else:
            erro = "Usuário ou senha incorretos."
            
    return render_template('login.html', erro=erro)

@app.route('/sair')
def sair():
    session.pop('logado', None) # Remove o login
    return redirect(url_for('login'))

# --- RESTANTE DO SEU CÓDIGO NORMAL ---

def ler_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {"tarefas": [], "estudos_agora": [], "estudos_proximos": []}
    with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

# ... (Mantenha aqui as suas rotas /api/dados, /api/tarefas e /api/excluir_tarefa exatamente como já estavam) ...

if __name__ == '__main__':
    app.run(debug=True)

app = Flask(__name__)
ARQUIVO_DADOS = 'dados.json'

def ler_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return {"tarefas": [], "estudos_agora": [], "estudos_proximos": []}
    with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    # Envia a página principal
    return render_template('index.html')

@app.route('/api/dados', methods=['GET'])
def obter_dados():
    # Envia os dados do JSON para o JavaScript
    return jsonify(ler_dados())

@app.route('/api/tarefas', methods=['POST'])
def adicionar_tarefa():
    dados = ler_dados()
    nova_tarefa = request.json
    dados['tarefas'].append(nova_tarefa)
    salvar_dados(dados)
    return jsonify({"status": "sucesso"})

@app.route('/api/excluir_tarefa', methods=['POST'])
def excluir_tarefa():
    id_tarefa = request.json.get('id')
    dados = ler_dados()
    # Filtra mantendo apenas as tarefas que não têm o ID que queremos excluir
    dados['tarefas'] = [t for t in dados['tarefas'] if t.get('id') != id_tarefa]
    salvar_dados(dados)
    return jsonify({"status": "sucesso"})

if __name__ == '__main__':
    app.run(debug=True)