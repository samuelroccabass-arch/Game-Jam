import mysql.connector
import bcrypt

DB_CONFIG = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "Senac2026",  # Altere para a sua senha do MySQL
    "database": "EcoMap"
}

def obter_conexao():
    return mysql.connector.connect(**DB_CONFIG)

def cadastrar_usuario(nome, senha):
    # Gera o hash seguro da senha
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash = bcrypt.hashpw(senha_bytes, salt).decode('utf-8')

    conn = obter_conexao()
    cursor = conn.cursor()

    try:
        # Verifica se o usuário já existe
        cursor.execute("SELECT id FROM usuarios WHERE nome = %s", (nome,))
        if cursor.fetchone():
            return False, "Nome de usuário já cadastrado."

        # Insere o novo usuário na tabela
        sql = "INSERT INTO usuarios (nome, senha_hash) VALUES (%s, %s)"
        cursor.execute(sql, (nome, senha_hash))
        conn.commit()
        return True, "Usuário cadastrado com sucesso!"

    except mysql.connector.Error as err:
        return False, f"Erro no banco de dados: {err}"
    finally:
        cursor.close()
        conn.close()

def autenticar_usuario(nome, senha):
    conn = obter_conexao()
    cursor = conn.cursor(dictionary=True)

    try:
        # Busca o usuário pelo nome
        cursor.execute("SELECT * FROM usuarios WHERE nome = %s", (nome,))
        usuario = cursor.fetchone()

        if not usuario:
            return False, "Usuário ou senha incorretos.", None

        # Valida a senha informada com o hash salvo no MySQL
        senha_bytes = senha.encode('utf-8')
        hash_salvo = usuario['senha_hash'].encode('utf-8')

        if bcrypt.checkpw(senha_bytes, hash_salvo):
            # Atualiza a coluna ultimo_acesso no MySQL
            cursor.execute(
                "UPDATE usuarios SET ultimo_acesso = NOW() WHERE id = %s", 
                (usuario['id'],)
            )
            conn.commit()

            dados_usuario = {
                "id": usuario['id'],
                "nome": usuario['nome']
            }
            return True, "Login realizado com sucesso!", dados_usuario
        else:
            return False, "Usuário ou senha incorretos.", None

    except mysql.connector.Error as err:
        return False, f"Erro no banco de dados: {err}", None
    finally:
        cursor.close()
        conn.close()