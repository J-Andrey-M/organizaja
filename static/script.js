// Controle de Abas
function mudarAba(aba) {
    document.getElementById('aba-tarefas').style.display = aba === 'tarefas' ? 'block' : 'none';
    document.getElementById('aba-estudos').style.display = aba === 'estudos' ? 'block' : 'none';
    
    let botoes = document.querySelectorAll('.tab-btn');
    botoes[0].classList.toggle('active', aba === 'tarefas');
    botoes[1].classList.toggle('active', aba === 'estudos');
}

// Carregar Tarefas do Backend
async function carregarTarefas() {
    const resposta = await fetch('/api/dados');
    const dados = await resposta.json();
    renderizarTarefas(dados.tarefas);
}

// Lógica de Cores baseada na Data
function calcularUrgencia(dataEntrega) {
    const hoje = new Date();
    hoje.setHours(0,0,0,0);
    const entrega = new Date(dataEntrega + 'T00:00:00'); // Fuso horário fixo
    
    const diferencaTempo = entrega.getTime() - hoje.getTime();
    const diasRestantes = Math.ceil(diferencaTempo / (1000 * 3600 * 24));

    if (diasRestantes <= 2) return { classe: 'urgencia-vermelha', texto: `${diasRestantes} dias (Urgente)` };
    if (diasRestantes === 3) return { classe: 'urgencia-amarela', texto: `3 dias (Atenção)` }; // Ajuste fino pra separar o amarelo
    if (diasRestantes >= 4 && diasRestantes <= 6) return { classe: 'urgencia-verde', texto: `${diasRestantes} dias` };
    return { classe: 'urgencia-azul', texto: `${diasRestantes} dias` }; // Mais de 6
}

function renderizarTarefas(tarefas) {
    const lista = document.getElementById('lista-tarefas');
    lista.innerHTML = ''; // Limpa a lista antes de desenhar

    // Ordenar para as mais urgentes (menor data) ficarem no topo
    tarefas.sort((a, b) => new Date(a.data) - new Date(b.data));

    tarefas.forEach(tarefa => {
        const urgencia = calcularUrgencia(tarefa.data);
        
        const card = document.createElement('div');
        card.className = `card ${urgencia.classe}`;
        
        card.innerHTML = `
            <h3>${tarefa.titulo}</h3>
            <p>Vence em: ${urgencia.texto} - (${tarefa.data})</p>
            <div class="card-actions">
                <button onclick="excluirTarefa(${tarefa.id})">Concluído / Excluir</button>
            </div>
        `;
        lista.appendChild(card);
    });
}

// Adicionar Nova Tarefa
async function adicionarTarefa() {
    const titulo = document.getElementById('titulo-tarefa').value;
    const data = document.getElementById('data-tarefa').value;

    if (!titulo || !data) {
        alert("Preencha título e data!");
        return;
    }

    const novaTarefa = {
        id: Date.now(), // Gera um ID único baseado na hora
        titulo: titulo,
        data: data
    };

    await fetch('/api/tarefas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(novaTarefa)
    });

    // Limpa os campos e recarrega a lista
    document.getElementById('titulo-tarefa').value = '';
    document.getElementById('data-tarefa').value = '';
    carregarTarefas();
}

// Excluir Tarefa
async function excluirTarefa(id) {
    await fetch('/api/excluir_tarefa', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
    });
    carregarTarefas();
}

// Inicia carregando as tarefas ao abrir a página
window.onload = carregarTarefas;