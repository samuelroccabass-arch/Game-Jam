function calcularDistancia(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
              Math.sin(dLon/2) * Math.sin(dLon/2);
    return R * (2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)));
}

function limparRota() {
    if (controleRota) {
        mapa.removeControl(controleRota);
        controleRota = null;
    }
}

function tracarRota(destLat, destLng) {
    if (!latUserAtual || !lngUserAtual) {
        alert("Pesquise um local ou ative o GPS primeiro.");
        return;
    }

    const urlGoogleMaps = `https://www.google.com/maps/dir/?api=1&origin=${latUserAtual},${lngUserAtual}&destination=${destLat},${destLng}&travelmode=driving`;
    window.open(urlGoogleMaps, '_blank');
}

function usarGPS() {
    if (!usuarioLogado) {
        verificarAutenticacao();
        return;
    }

    if (!navigator.geolocation) {
        alert("Geolocalização não é suportada pelo seu navegador.");
        return;
    }

    const divLista = document.getElementById('listaPontos');
    divLista.innerHTML = `<div class="empty-state"><div></div><p>Obtendo sua localização atual...</p></div>`;

    navigator.geolocation.getCurrentPosition(
        (posicao) => {
            const lat = posicao.coords.latitude;
            const lng = posicao.coords.longitude;
            
            document.getElementById('inputEndereco').value = "Minha Localização (GPS)";
            buscarPontosPorCoordenadas(lat, lng);
        },
        (erro) => {
            alert("Não foi possível obter sua localização. Verifique as permissões do seu navegador.");
            divLista.innerHTML = `<div class="empty-state"><div></div><p>Permissão de localização negada.</p></div>`;
        }
    );
}

function renderizarListaEPontos(pontos) {
    const divLista = document.getElementById('listaPontos');
    divLista.innerHTML = "";

    pontos.forEach((ponto, index) => {
        const numero = index + 1;
        const distFormatada = ponto.distancia < 1 
            ? `${Math.round(ponto.distancia * 1000)}m` 
            : `${ponto.distancia.toFixed(1)} km`;

        const tagsHtml = ponto.materiais.map(m => `<span class="tag">♻️ ${m}</span>`).join('');

        const m = L.marker([ponto.lat, ponto.lng]).addTo(mapa);
        
        m.bindTooltip(`<b>#${numero} ${ponto.nome}</b>`, {
            permanent: false,
            direction: 'top'
        });

        m.bindPopup(`
            <div style="font-family: 'Inter', sans-serif;">
                <b style="color: #10b981;">#${numero} - ${ponto.nome}</b><br>
                <small> a ${distFormatada} de você</small><br><br>
                <b>Materiais:</b><br>${tagsHtml}<br><br>
                <button onclick="tracarRota(${ponto.lat}, ${ponto.lng})" style="width:100%; padding:6px; background:#3b82f6; color:white; border:none; border-radius:4px; font-weight:600; cursor:pointer;">🗺️ Traçar Rota</button>
            </div>
        `);

        marcadores.push(m);

        const card = document.createElement('div');
        card.className = 'card-ponto';
        card.innerHTML = `
            <div class="card-header-flex">
                <span class="numero-badge">${numero}</span>
                <h3>${ponto.nome}</h3>
            </div>
            <div class="distancia-badge"> a ${distFormatada} de você</div>
            <div class="cidade-texto">${ponto.cidade}</div>
            <div class="tags-container">${tagsHtml}</div>
            <button class="btn-rota" onclick="event.stopPropagation(); tracarRota(${ponto.lat}, ${ponto.lng})"> Como Chegar</button>
        `;

        card.onclick = () => {
            mapa.setView([ponto.lat, ponto.lng], 15);
            m.openPopup();
        };

        divLista.appendChild(card);
    });
}