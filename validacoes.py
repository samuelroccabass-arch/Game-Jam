import re
 
def validar_nome(nome):
    """
    Verifica se o nome (nome + sobrenome) é válido:
    - Pelo menos 2 caracteres
    - Tem pelo menos duas palavras (nome e sobrenome)
    """
    if not nome or len(nome.strip()) < 2:
        return False, "O nome deve ter pelo menos 2 caracteres."
    if len(nome.strip().split()) < 2:
        return False, "Digite o nome e o sobrenome."
    return True, ""
 
def validar_senha(senha):
    """
    Verifica se a senha é forte o suficiente:
    - Pelo menos 6 caracteres
    - Pelo menos 1 letra e 1 número
    """
    if not senha or len(senha) < 6:
        return False, "A senha deve ter pelo menos 6 caracteres."
    if not re.search(r"[A-Za-z]", senha) or not re.search(r"[0-9]", senha):
        return False, "A senha deve conter letras e números."
    return True, ""
 
def validar_cadastro(nome, senha):
    """
    Roda todas as validações de uma vez.
    Retorna (True, "") se tudo estiver ok, ou (False, "mensagem do erro").
    """
    ok, msg = validar_nome(nome)
    if not ok:
        return False, msg
 
    ok, msg = validar_senha(senha)
    if not ok:
        return False, msg
 
    return True, ""
 