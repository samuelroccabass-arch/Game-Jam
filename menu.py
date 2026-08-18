import main
from conector_mysql import conectar
cursor = conectar().cursor()

def menu ():
    while True:
        print("\n=====EcoPalhoca=====")
        print("1. Consultar material")
        print("2. Listar pontos de coleta")
        print("3. Cadastrar ponto de coleta")
        print("4. Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            main.consultar_material(cursor)
            
        elif opcao == "2":
            main.listar_pontos(cursor)
        elif opcao == "3":
            main.cadastro_material(cursor)
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")


menu(cursor, conectar)
cursor.close()
conectar.close()