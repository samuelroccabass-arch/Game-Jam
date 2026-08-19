// Variáveis globais compartilhadas pelos módulos
const mapa = L.map('mapa').setView([-14.2350, -51.9253], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
}).addTo(mapa);

let marcadores = [];
let usuarioLogado = null;
let controleRota = null;
let latUserAtual = null;
let lngUserAtual = null;

window.addEventListener('DOMContentLoaded', () => {
    verificarAutenticacao();
});

function alternarTema() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    const newTheme = isDark ? 'light' : 'dark';
    
    html.setAttribute('data-theme', newTheme);
    document.getElementById('themeIcon').innerText = newTheme === 'dark' ? '☀️' : '🌙';
    document.getElementById('themeText').innerText = newTheme === 'dark' ? 'Claro' : 'Escuro';
}

function tratarEnter(e) {
    if (e.key === 'Enter') buscarPontos();
}