async function executarLogin() {
    const nome = document.getElementById('loginNome').value.trim();
    const senha = document.getElementById('loginSenha').value;
    const msg = document.getElementById('msgLogin');

    if (!nome || !senha) {
        msg.className = 'modal-msg msg-erro';
        msg.innerText = 'Preencha o nome e a senha.';
        return;
    }

    msg.className = 'modal-msg';
    msg.innerText = 'Verificando...';

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, senha })
        });
        const dados = await response.json();

        if (!response.ok) {
            msg.className = 'modal-msg msg-erro';
            msg.innerText = dados.erro || 'Erro ao entrar.';
            return;
        }

        usuarioLogado = dados.usuario.nome;
        document.getElementById('btnAuth').innerText = `👤 ${usuarioLogado.split(' ')[0]}`;
        
        const modal = document.getElementById('modalAuth');
        modal.classList.remove('forcar-login');
        modal.style.display = 'none';
        document.getElementById('mapa').style.pointerEvents = 'auto';

        document.getElementById('loginNome').value = '';
        document.getElementById('loginSenha').value = '';
        msg.innerText = '';

    } catch (err) {
        msg.className = 'modal-msg msg-erro';
        msg.innerText = 'Falha de conexão com o servidor.';
    }
}

async function executarCadastro() {
    const nome = document.getElementById('cadNome').value.trim();
    const senha = document.getElementById('cadSenha').value;
    const msg = document.getElementById('msgCad');

    if (!nome || !senha) {
        msg.className = 'modal-msg msg-erro';
        msg.innerText = 'Preencha todos os campos.';
        return;
    }

    msg.className = 'modal-msg';
    msg.innerText = 'Cadastrando...';

    try {
        const response = await fetch('/cadastro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, senha })
        });
        const dados = await response.json();

        if (!response.ok) {
            msg.className = 'modal-msg msg-erro';
            msg.innerText = dados.erro || 'Erro no cadastro.';
            return;
        }

        msg.className = 'modal-msg msg-sucesso';
        msg.innerText = 'Cadastrado com sucesso! Redirecionando...';
        
        setTimeout(() => {
            alternarFormAuth('login');
            document.getElementById('loginNome').value = nome;
            document.getElementById('cadNome').value = '';
            document.getElementById('cadSenha').value = '';
        }, 1200);

    } catch (err) {
        msg.className = 'modal-msg msg-erro';
        msg.innerText = 'Falha de conexão com o servidor.';
    }
}

async function buscarPontosPorCoordenadas(lat, lng) {
    limparRota();
    marcadores.forEach(m => mapa.removeLayer(m));
    marcadores = [];

    const divLista = document.getElementById('listaPontos');
    divLista.innerHTML = `<div class="empty-state"><div>⏳</div><p>Carregando ecopontos...</p></div>`;

    try {
        const res = await fetch(`/buscar?lat=${lat}&lng=${lng}`);
        const dados = await res.json();

        if (dados.erro) {
            divLista.innerHTML = `<div class="empty-state"><div>⚠️</div><p>${dados.erro}</p></div>`;
            return;
        }

        latUserAtual = dados.lat_usuario;
        lngUserAtual = dados.lng_usuario;

        mapa.setView([latUserAtual, lngUserAtual], 13);

        const userMarker = L.marker([latUserAtual, lngUserAtual]).addTo(mapa)
            .bindPopup("<b>📍 Sua Localização Atual</b>").openPopup();
        marcadores.push(userMarker);

        if (!dados.pontos || dados.pontos.length === 0) {
            divLista.innerHTML = `<div class="empty-state"><div>📦</div><p>Nenhum ponto registrado nessa área.</p></div>`;
            return;
        }

        dados.pontos.forEach(ponto => {
            ponto.distancia = calcularDistancia(latUserAtual, lngUserAtual, ponto.lat, ponto.lng);
        });
        dados.pontos.sort((a, b) => a.distancia - b.distancia);

        renderizarListaEPontos(dados.pontos);

    } catch (err) {
        console.error(err);
        divLista.innerHTML = `<div class="empty-state"><div>❌</div><p>Erro de conexão com o servidor.</p></div>`;
    }
}

async function buscarPontos() {
    if (!usuarioLogado) {
        verificarAutenticacao();
        return;
    }

    const input = document.getElementById('inputEndereco');
    const endereco = input.value.trim();
    if (!endereco) return alert("Por favor, digite um endereço!");

    limparRota();
    marcadores.forEach(m => mapa.removeLayer(m));
    marcadores = [];

    const divLista = document.getElementById('listaPontos');
    divLista.innerHTML = `<div class="empty-state"><div>⏳</div><p>Carregando ecopontos...</p></div>`;

    try {
        const res = await fetch(`/buscar?endereco=${encodeURIComponent(endereco)}`);
        const dados = await res.json();

        if (dados.erro) {
            divLista.innerHTML = `<div class="empty-state"><div>⚠️</div><p>${dados.erro}</p></div>`;
            return;
        }

        latUserAtual = dados.lat_usuario;
        lngUserAtual = dados.lng_usuario;

        mapa.setView([latUserAtual, lngUserAtual], 12);

        const userMarker = L.marker([latUserAtual, lngUserAtual]).addTo(mapa)
            .bindPopup("<b>📍 Ponto de Origem</b>").openPopup();
        marcadores.push(userMarker);

        if (!dados.pontos || dados.pontos.length === 0) {
            divLista.innerHTML = `<div class="empty-state"><div>📦</div><p>Nenhum ponto registrado nessa área.</p></div>`;
            return;
        }

        dados.pontos.forEach(ponto => {
            ponto.distancia = calcularDistancia(latUserAtual, lngUserAtual, ponto.lat, ponto.lng);
        });
        dados.pontos.sort((a, b) => a.distancia - b.distancia);

        renderizarListaEPontos(dados.pontos);

    } catch (err) {
        console.error(err);
        divLista.innerHTML = `<div class="empty-state"><div>❌</div><p>Erro de conexão com o servidor.</p></div>`;
    }
}async function buscarPontos() {
    if (!usuarioLogado) {
        verificarAutenticacao();
        return;
    }

    const input = document.getElementById('inputEndereco');
    const endereco = input.value.trim();
    if (!endereco) return alert("Por favor, digite um endereço!");

    // 1. Limpa marcadores e estado anterior antes de qualquer requisição
    limparRota();
    marcadores.forEach(m => mapa.removeLayer(m));
    marcadores = [];

    const divLista = document.getElementById('listaPontos');
    divLista.innerHTML = `<div class="empty-state"><div>⏳</div><p>Localizando "${endereco}"...</p></div>`;

    try {
        // 2. Faz a requisição para o backend para buscar o endereço
        const res = await fetch(`/buscar?endereco=${encodeURIComponent(endereco)}`);
        const dados = await res.json();

        if (dados.erro) {
            divLista.innerHTML = `<div class="empty-state"><div>⚠️</div><p>${dados.erro}</p></div>`;
            return;
        }

        // 3. Atualiza FORÇADAMENTE as coordenadas globais antes de renderizar
        latUserAtual = parseFloat(dados.lat_usuario);
        lngUserAtual = parseFloat(dados.lng_usuario);

        // 4. Centraliza o mapa e força a renderização imediata na nova coordenada
        mapa.setView([latUserAtual, lngUserAtual], 12, { animate: false });

        const userMarker = L.marker([latUserAtual, lngUserAtual]).addTo(mapa)
            .bindPopup(`<b>📍 Origem: ${endereco}</b>`).openPopup();
        marcadores.push(userMarker);

        if (!dados.pontos || dados.pontos.length === 0) {
            divLista.innerHTML = `<div class="empty-state"><div>📦</div><p>Nenhum ponto encontrado em um raio de 15km nessa região.</p></div>`;
            return;
        }

        // 5. Recalcula as distâncias com base no NOVO centro
        dados.pontos.forEach(ponto => {
            ponto.distancia = calcularDistancia(latUserAtual, lngUserAtual, ponto.lat, ponto.lng);
        });
        dados.pontos.sort((a, b) => a.distancia - b.distancia);

        renderizarListaEPontos(dados.pontos);

    } catch (err) {
        console.error(err);
        divLista.innerHTML = `<div class="empty-state"><div>❌</div><p>Erro de conexão com o servidor.</p></div>`;
    }
}