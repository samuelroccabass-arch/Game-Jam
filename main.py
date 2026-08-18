import mysql.connector
from conector_mysql import conectar

cursor = conectar().cursor()

def consultar_material(cursor):
    material = input("Digite o nome do material): ").strip()
    sql = "SELECT nome, categoria,destino From materiais WHERE nome = %s"
    cursor.execute(sql, (material,))
    resultado = cursor.fetchone()
    if resultado:
        for nome, categoria, destino in [resultado]:
            print(f"Nome: {nome}")
            print(f"Categoria: {categoria}")
            print(f"Destino: {destino}")

    else:
        print("Material não encontrado.")

def listar_pontos(cursor):
    sql = "SELECT nome, bairro, endereco, cidade FROM materiais_aceitos"
    cursor.execute(sql)
    resultados = cursor.fetchall()

    if resultados:
        for nome, bairro, endereco, cidade in resultados:
            print(f"Nome: {nome}")
            print(f"Bairro: {bairro}")
            print(f"Endereço: {endereco}")
            print(f"Cidade: {cidade}")

    else:
        print("Nenhum ponto de coleta encontrado.")

def cadastro_material(cursor):
    nome = input("Digite o nome do material: ").strip()
    bairro = input("Digite o bairro do ponto de coleta: ").strip()
    endereco = input("Digite o endereço do ponto de coleta: ").strip()
    materiais_aceitos = input("Digite os materiais aceitos (separados por vírgula): ").strip()
    cidade = input("Digite a cidade do ponto de coleta: ").strip()

    sql = """
    INSERT INTO materiais_aceitos (nome, bairro, endereco, cidade, materiais_aceitos) 
    VALUES (%s, %s, %s, %s, %s)"
    """
    valores = (nome, bairro, endereco, cidade, materiais_aceitos)
    cursor().execute(sql, valores) 
    conectar().commit()

    print("Ponto de coleta cadastrado com sucesso!")

