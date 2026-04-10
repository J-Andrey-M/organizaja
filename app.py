from flask import Flask, render_template, request, jsonify
import json
import os

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