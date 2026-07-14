import json
import os
import getpass
from datetime import datetime
from Camara import tirarFoto

# =====================================================
# CONFIGURAÇÕES
# =====================================================

ARQUIVO = "C:/Temp/MinhaPasta/utilizadores.txt"
ARQUIVO_LOG = "C:/Temp/MinhaPasta/logs.txt"

utilizadores = []

# =====================================================
# INICIALIZAÇÃO
# =====================================================

def inicializar():
    """Inicializa o módulo carregando os utilizadores."""
    carregar_utilizadores()
    print("\nMódulo de Utilizadores iniciado com sucesso!")


# =====================================================
# GUARDAR UTILIZADORES
# =====================================================

def guardar_utilizadores():
    try:
        with open(ARQUIVO, "w", encoding="utf-8") as ficheiro:
            json.dump(utilizadores, ficheiro, indent=4, ensure_ascii=False)
    except Exception as erro:
        print(f"\nErro ao guardar utilizadores: {erro}")

def escrever_log(evento):
    with open(ARQUIVO_LOG, "a", encoding="utf-8") as ficheiro:
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        ficheiro.write(f"{data} - {evento}\n")


# =====================================================
# CARREGAR UTILIZADORES
# =====================================================

def carregar_utilizadores():
    global utilizadores

    if not os.path.exists(ARQUIVO):
        utilizadores = []
        guardar_utilizadores()
        return

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as ficheiro:
            utilizadores = json.load(ficheiro)
    except:
        utilizadores = []

# =====================================================
# GERAR ID
# =====================================================

def gerar_id():

    if not utilizadores:
        return 1

    maior = max(utilizador["id"] for utilizador in utilizadores)
    return maior + 1


# =====================================================
# PAUSA
# =====================================================

def pausar():
    input("\nPrima ENTER para continuar...")


# =====================================================
# VERIFICAR USERNAME
# =====================================================

def username_existe(username):

    for utilizador in utilizadores:
        if utilizador["username"].lower() == username.lower():
            return True

    return False


# =====================================================
# CRIAR UTILIZADOR
# =====================================================

def criar_utilizador():

    print("\n========== CRIAR UTILIZADOR ==========")

    while True:

        nome = input("Nome: ").strip()

        if nome:
            break

        print("O nome não pode estar vazio.")

    while True:

        username = input("Username: ").strip()

        if not username:
            print("O username não pode estar vazio.")
            continue

        if username_existe(username):
            print("Esse username já existe.")
            continue

        break

    while True:

        password = getpass.getpass("Password: ").strip()

        if password:
            break

        print("A password não pode estar vazia.")

    while True:

        print("\nTipos disponíveis:")
        print("1 - Administrador")
        print("2 - Utilizador")

        opcao = input("Escolha: ")

        if opcao == "1":
            tipo = "Administrador"
            break

        elif opcao == "2":
            tipo = "Utilizador"
            break

        else:
            print("Opção inválida.")

# ==========================
# REGISTO DO FACE ID
# ==========================

    print("\n REGISTO DE FACE ID")
    print("=" * 50)

    input("Prima ENTER para abrir a câmara...")
    print("Vou abrir a câmara...")
    caminho_foto = tirarFoto(username)

    print("\n Face ID capturado com sucesso!")
    utilizador = {
        "id": gerar_id(),
        "nome": nome,
        "username": username,
        "password": password,
        "tipo": tipo,
        "foto": caminho_foto
    }

    utilizadores.append(utilizador)

    guardar_utilizadores()
    escrever_log(f"Utilizador {username} criado.")
    print("\nUtilizador criado com sucesso!")

    pausar()
    # =====================================================
# LISTAR UTILIZADORES
# =====================================================

def listar_utilizadores():

    if not utilizadores:
        print("\nNão existem utilizadores registados.")
        pausar()
        return

    print("\n========== LISTA DE UTILIZADORES ==========")

    lista_ordenada = sorted(utilizadores, key=lambda x: x["nome"].lower())

    for utilizador in lista_ordenada:

        print("------------------------------------------")
        print(f"ID: {utilizador['id']}")
        print(f"Nome: {utilizador['nome']}")
        print(f"Username: {utilizador['username']}")
        print(f"Password: {'*' * len(utilizador['password'])}")
        print(f"Tipo: {utilizador['tipo']}")

    print("------------------------------------------")

    pausar()

# =====================================================
# EDITAR UTILIZADOR
# =====================================================

def editar_utilizador():

    if not utilizadores:
        print("\nNão existem utilizadores registados.")
        pausar()
        return

    username = input("\nUsername do utilizador: ").strip()

    for utilizador in utilizadores:

        if utilizador["username"].lower() == username.lower():

            print("\nPrima ENTER para manter o valor atual.\n")

            novo_nome = input(f"Nome ({utilizador['nome']}): ").strip()

            while True:

                novo_username = input(
                    f"Username ({utilizador['username']}): "
                ).strip()

                if not novo_username:
                    break

                existe = False

                for outro in utilizadores:

                    if (
                        outro["username"].lower() == novo_username.lower()
                        and outro["id"] != utilizador["id"]
                    ):
                        existe = True
                        break

                if existe:
                    print("Esse username já existe.")
                else:
                    break

            nova_password = getpass.getpass(
                "Nova password (ENTER para manter): "
            ).strip()

            while True:

                print("\nTipo:")
                print("1 - Administrador")
                print("2 - Utilizador")
                print("ENTER - Manter")

                opcao = input("Escolha: ").strip()

                if opcao == "":
                    novo_tipo = utilizador["tipo"]
                    break

                elif opcao == "1":
                    novo_tipo = "Administrador"
                    break

                elif opcao == "2":
                    novo_tipo = "Utilizador"
                    break

                else:
                    print("Opção inválida.")

            if novo_nome:
                utilizador["nome"] = novo_nome

            if novo_username:
                utilizador["username"] = novo_username

            if nova_password:
                utilizador["password"] = nova_password

            utilizador["tipo"] = novo_tipo

            guardar_utilizadores()
            escrever_log(f"Utilizador {utilizador['username']} editado.")
            print("\nUtilizador atualizado com sucesso!")

            pausar()
            return

    print("\nUtilizador não encontrado.")
    pausar()


# =====================================================
# ELIMINAR UTILIZADOR
# =====================================================

def eliminar_utilizador():

    if not utilizadores:
        print("\nNão existem utilizadores registados.")
        pausar()
        return

    username = input("\nUsername do utilizador: ").strip()

    for utilizador in utilizadores:

        if utilizador["username"].lower() == username.lower():

            print("\n========== UTILIZADOR ==========")
            print(f"Nome: {utilizador['nome']}")
            print(f"Username: {utilizador['username']}")
            print(f"Tipo: {utilizador['tipo']}")

            confirmar = input(
                "\nTem a certeza que pretende eliminar este utilizador? (S/N): "
            ).strip().upper()

            if confirmar == "S":

                utilizadores.remove(utilizador)
                guardar_utilizadores()
                escrever_log(f"Utilizador {utilizador['username']} eliminado.")
                print("\nUtilizador eliminado com sucesso!")

            else:

                print("\nOperação cancelada.")

            pausar()
            return

    print("\nUtilizador não encontrado.")
    pausar()


# =====================================================
# ESTATÍSTICAS
# =====================================================

def estatisticas():

    total = len(utilizadores)

    administradores = 0
    utilizadores_normais = 0

    for utilizador in utilizadores:

        if utilizador["tipo"] == "Administrador":
            administradores += 1
        else:
            utilizadores_normais += 1

    print("\n========== ESTATÍSTICAS ==========")
    print(f"Total de utilizadores: {total}")
    print(f"Administradores: {administradores}")
    print(f"Utilizadores: {utilizadores_normais}")

    pausar()
# =====================================================
# MENU
# =====================================================
def ver_logs():

    if not os.path.exists(ARQUIVO_LOG):
        print("\nAinda não existem logs.")
        pausar()
        return

    print("\n========== LOGS DO SISTEMA ==========\n")

    with open(ARQUIVO_LOG, "r", encoding="utf-8") as ficheiro:
        print(ficheiro.read())

    pausar()

def menu():

    while True:

        print("\n====================================")
        print("      GESTÃO DE UTILIZADORES")
        print("====================================")
        print("1 - Criar utilizador")
        print("2 - Listar utilizadores")
        print("3 - Editar utilizador")
        print("4 - Eliminar utilizador")
        print("5 - Estatísticas")
        print("6 - Ver Logs")
        print("0 - Sair")
        print("====================================")

        opcao = input("Escolha uma opção: ").strip()

        try:

            if opcao == "1":
                criar_utilizador()

            elif opcao == "2":
                listar_utilizadores()

            elif opcao == "3":
                editar_utilizador()

            elif opcao == "4":
                eliminar_utilizador()

            elif opcao == "5":
                estatisticas()
            
            elif opcao == "6":
                ver_logs()

            elif opcao == "0":
                print("\nA encerrar o módulo de Utilizadores...")
                break

            else:
                print("\nOpção inválida.")
                pausar()

        except Exception as erro:
            print(f"\nOcorreu um erro: {erro}")
            pausar()


# =====================================================
# EXECUTOR
# =====================================================

def executar():
    inicializar()
    menu()


# =====================================================
# ENTRY POINT
# =====================================================

if __name__ == "__main__":
    executar()
    