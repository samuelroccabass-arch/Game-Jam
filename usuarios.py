import hashlib
import mysql.connector
from mysql.connector import Error
 
# ==============================================================================
#  CONFIGURAÇÃO DO BANCO
# ==============================================================================
DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Senac2026",
    "database": "EcoPalhoca"
}
 
 
def get_conexao():
    """Abre e retorna uma conexão com o banco. Retorna None se falhar."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f" Erro ao conectar no MySQL: {e}")
        return None
 
 
def hash_senha(senha):
    """
    Gera um hash da senha com SHA-256.
    Obs: para um projeto mais robusto, o ideal é usar a lib 'bcrypt'
    (pip install bcrypt), que é mais segura que SHA-256 puro.
    """
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()
 
 
def cadastrar_usuario(nome, senha):
    """
    Insere um novo usuário no banco.
    Retorna (True, "mensagem de sucesso") ou (False, "mensagem de erro").
    """
    conn = get_conexao()
    if not conn:
        return False, "Não foi possível conectar ao banco de dados."
 
    try:
        cursor = conn.cursor()
        senha_criptografada = hash_senha(senha)
        cursor.execute(
            "INSERT INTO usuarios (nome, senha_hash) VALUES (%s, %s)",
            (nome, senha_criptografada)
        )
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"
    except Error as e:
        return False, f"Erro ao cadastrar: {e}"
    finally:
        cursor.close()
        conn.close()
 
 
def autenticar_usuario(nome, senha):
    """
    Verifica se o nome e senha batem com um usuário do banco.
    Retorna (True, dados_do_usuario) ou (False, "mensagem de erro").
    """
    conn = get_conexao()
    if not conn:
        return False, "Não foi possível conectar ao banco de dados."
 
    try:
        cursor = conn.cursor(dictionary=True)
        senha_criptografada = hash_senha(senha)
        cursor.execute(
            "SELECT id, nome FROM usuarios WHERE nome = %s AND senha_hash = %s",
            (nome, senha_criptografada)
        )
        usuario = cursor.fetchone()
 
        if usuario:
            # Atualiza o último acesso
            cursor.execute(
                "UPDATE usuarios SET ultimo_acesso = NOW() WHERE id = %s",
                (usuario["id"],)
            )
            conn.commit()
            return True, usuario
        else:
            return False, "Nome ou senha incorretos."
    finally:
        cursor.close()
        conn.close()
 
 
def listar_usuarios():
    """Retorna todos os usuários cadastrados (sem a senha)."""
    conn = get_conexao()
    if not conn:
        return []
 
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, data_cadastro, ultimo_acesso FROM usuarios")
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()