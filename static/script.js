// Controle de Abas
function mudarAba(aba) {
    document.getElementById('aba-tarefas').style.display = aba === 'tarefas' ? 'block' : 'none';
    document.getElementById('aba-estudos').style.display = aba === 'estudos' ? 'block' : 'none';
    
    let botoes = document.querySelectorAll('.tab-btn');
    botoes[0].classList.toggle('active', aba === 'tarefas');
    botoes[1].classList.toggle('active', aba === 'estudos');
}

// --- LÓGICA DE DADOS (LOCAL STORAGE) ---
function obterTarefas() {
    const tarefasSalvas = localStorage.getItem('minhas_tarefas');
    return tarefasSalvas ? JSON.parse(tarefasSalvas) : [];
}

function salvarTarefas(tarefas) {
    localStorage.setItem('minhas_tarefas', JSON.stringify(tarefas));
}

// Lógica de Cores baseada na Data
function calcularUrgencia(dataEntrega) {
    const hoje = new Date();
    hoje.setHours(0,0,0,0);
    const entrega = new Date(dataEntrega + 'T00:00:00');
    
    const diferencaTempo = entrega.getTime() - hoje.getTime();
    const diasRestantes = Math.ceil(diferencaTempo / (1000 * 3600 * 24));

    if (diasRestantes <= 2) return { classe: 'urgencia-vermelha', texto: `${diasRestantes} dias (Urgente)` };
    if (diasRestantes === 3) return { classe: 'urgencia-amarela', texto: `3 dias (Atenção)` };
    if (diasRestantes >= 4 && diasRestantes <= 6) return { classe: 'urgencia-verde', texto: `${diasRestantes} dias` };
    return { classe: 'urgencia-azul', texto: `${diasRestantes} dias` };
}

function renderizarTarefas() {
    const tarefas = obterTarefas();
    const lista = document.getElementById('lista-tarefas');
    lista.innerHTML = ''; 

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

function adicionarTarefa() {
    const titulo = document.getElementById('titulo-tarefa').value;
    const data = document.getElementById('data-tarefa').value;

    if (!titulo || !data) {
        alert("Preencha título e data!");
        return;
    }

    const tarefas = obterTarefas();
    const novaTarefa = {
        id: Date.now(),
        titulo: titulo,
        data: data
    };

    tarefas.push(novaTarefa);
    salvarTarefas(tarefas);

    document.getElementById('titulo-tarefa').value = '';
    document.getElementById('data-tarefa').value = '';
    renderizarTarefas();
}

function excluirTarefa(id) {
    let tarefas = obterTarefas();
    tarefas = tarefas.filter(t => t.id !== id);
    salvarTarefas(tarefas);
    renderizarTarefas();
}

// Inicia carregando as tarefas
window.onload = renderizarTarefas;