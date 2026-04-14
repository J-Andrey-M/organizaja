from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('CHAVE_SECRETA', 'chave_padrao') 

ARQUIVO_DADOS = 'dados.json'

@app.before_request
def verificar_login():
    if request.endpoint not in ['login', 'static'] and 'logado' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        usuario_digitado = request.form.get('usuario')
        senha_digitada = request.form.get('senha')
        
        if usuario_digitado == os.getenv('MEU_USUARIO') and senha_digitada == os.getenv('MINHA_SENHA'):
            session['logado'] = True
            return redirect(url_for('index'))
        else:
            erro = "Usuário ou senha incorretos."
            
    return render_template('login.html', erro=erro)

@app.route('/sair')
def sair():
    session.pop('logado', None)
    return redirect(url_for('login'))

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

@app.route('/api/dados', methods=['GET'])
def obter_dados():
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
    dados['tarefas'] = [t for t in dados['tarefas'] if t.get('id') != id_tarefa]
    salvar_dados(dados)
    return jsonify({"status": "sucesso"})

if __name__ == '__main__':
    app.run(debug=True)