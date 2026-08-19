from flask import request, jsonify
from validacoes import validar_cadastro
from usuarios import cadastrar_usuario, autenticar_usuario
 
 
def registrar_rotas_usuario(app):
    """
    Registra as rotas de cadastro e login no app Flask.
    No seu app.py, depois de criar o `app = Flask(__name__)`, chame:
 
        from rotas_usuarios import registrar_rotas_usuario
        registrar_rotas_usuario(app)
    """
 
    @app.route("/cadastro", methods=["POST"])
    def cadastro():
        dados = request.get_json(silent=True) or request.form
        nome = dados.get("nome", "").strip()
        senha = dados.get("senha", "")
 
        valido, mensagem = validar_cadastro(nome, senha)
        if not valido:
            return jsonify({"erro": mensagem}), 400
 
        sucesso, mensagem = cadastrar_usuario(nome, senha)
        if not sucesso:
            return jsonify({"erro": mensagem}), 400
 
        return jsonify({"mensagem": mensagem}), 201
 
    @app.route("/login", methods=["POST"])
    def login():
        dados = request.get_json(silent=True) or request.form
        nome = dados.get("nome", "").strip()
        senha = dados.get("senha", "")
 
        if not nome or not senha:
            return jsonify({"erro": "Informe nome e senha."}), 400
 
        sucesso, resultado = autenticar_usuario(nome, senha)
        if not sucesso:
            return jsonify({"erro": resultado}), 401
 
        return jsonify({"mensagem": "Login realizado com sucesso!", "usuario": resultado}), 200
 
    return app
 