function verificarAutenticacao() {
    if (!usuarioLogado) {
        const modal = document.getElementById('modalAuth');
        modal.classList.add('forcar-login');
        modal.style.display = 'flex';
        document.getElementById('mapa').style.pointerEvents = 'none';
    }
}

function abrirModalAuth() {
    if (usuarioLogado) {
        if (confirm(`Deseja sair da conta de ${usuarioLogado}?`)) {
            usuarioLogado = null;
            document.getElementById('btnAuth').innerText = "Entrar";
            verificarAutenticacao();
        }
        return;
    }
    document.getElementById('modalAuth').style.display = 'flex';
}

function fecharModalAuth() {
    if (!usuarioLogado) {
        alert("Você precisa realizar o login ou cadastrar-se para usar a aplicação.");
        return;
    }
    document.getElementById('modalAuth').style.display = 'none';
}

function alternarFormAuth(tipo) {
    document.getElementById('msgLogin').innerText = '';
    document.getElementById('msgCad').innerText = '';
    if (tipo === 'cadastro') {
        document.getElementById('formLogin').style.display = 'none';
        document.getElementById('formCadastro').style.display = 'block';
    } else {
        document.getElementById('formCadastro').style.display = 'none';
        document.getElementById('formLogin').style.display = 'block';
    }
}