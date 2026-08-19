from flask import request, jsonify
from usuarios import cadastrar_usuario, autenticar_usuario

def registrar_rotas_usuario(app):

    @app.route("/cadastro", methods=["POST"])
    def rota_cadastro():
        dados = request.get_json() or {}
        nome = dados.get("nome", "").strip()
        senha = dados.get("senha", "")

        # Validações básicas de entrada
        if not nome or not senha:
            return jsonify({"erro": "Nome e senha são obrigatórios."}), 400

        if len(senha) < 6:
            return jsonify({"erro": "A senha deve ter pelo menos 6 caracteres."}), 400

        sucesso, mensagem = cadastrar_usuario(nome, senha)

        if sucesso:
            return jsonify({"mensagem": mensagem}), 201
        else:
            return jsonify({"erro": mensagem}), 400

    @app.route("/login", methods=["POST"])
    def rota_login():
        dados = request.get_json() or {}
        nome = dados.get("nome", "").strip()
        senha = dados.get("senha", "")

        if not nome or not senha:
            return jsonify({"erro": "Informe o nome e a senha."}), 400

        sucesso, mensagem, usuario = autenticar_usuario(nome, senha)

        if sucesso:
            return jsonify({"mensagem": mensagem, "usuario": usuario}), 200
        else:
            return jsonify({"erro": mensagem}), 401