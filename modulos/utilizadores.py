import getpass

from base_dados import utilizadores_db

from modulos import registos
from modulos.Camara import tirarFoto


def inicializar():
    """Confirma que a base de dados está acessível."""
    print(
        f"\nMódulo de Utilizadores iniciado! {utilizadores_db.contar()} conta(s) registada(s)."
    )


def username_existe(username):
    return utilizadores_db.existe(username)


def criar(nome, username, password, tipo="Utilizador", foto=None):
    """Cria um utilizador e devolve o id atribuído."""
    id_utilizador = utilizadores_db.criar(nome, username, password, tipo, foto)

    registos.escrever(f"Utilizador {username} criado.")

    return id_utilizador


def obter(username):
    return utilizadores_db.obter(username)


def obter_por_id(id_utilizador):
    return utilizadores_db.obter_por_id(id_utilizador)


def listar():
    return utilizadores_db.listar()


def editar(username, nome=None, novo_username=None, password=None, tipo=None):
    """Atualiza os campos indicados. Campos vazios mantêm o valor atual."""
    if utilizadores_db.atualizar(username, {
        "nome": nome,
        "username": novo_username,
        "password": password,
        "tipo": tipo
    }):
        registos.escrever(f"Utilizador {username} editado.")

        return True

    return False


def eliminar(username):
    if utilizadores_db.eliminar(username):
        registos.escrever(f"Utilizador {username} eliminado.")

        return True

    return False


def resumo():
    """Conta utilizadores por tipo."""
    lista = utilizadores_db.listar()

    administradores = len([u for u in lista if u["tipo"] == "Administrador"])

    return {
        "total": len(lista),
        "administradores": administradores,
        "utilizadores": len(lista) - administradores
    }


def pausar():
    input("\nPrima ENTER para continuar...")


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

    print("\n REGISTO DE FACE ID")
    print("=" * 50)

    input("Prima ENTER para abrir a câmara...")
    print("Vou abrir a câmara...")
    caminho_foto = tirarFoto(username)

    criar(nome, username, password, tipo, caminho_foto)

    print("\nFace ID capturado com sucesso!")
    print("\nUtilizador criado com sucesso!")

    pausar()


def listar_utilizadores():
    lista = utilizadores_db.listar()

    if not lista:
        print("\nNão existem utilizadores registados.")
        pausar()
        return

    print("\n========== LISTA DE UTILIZADORES ==========")

    for utilizador in sorted(lista, key=lambda x: x["nome"].lower()):

        print("------------------------------------------")
        print(f"ID: {utilizador['id']}")
        print(f"Nome: {utilizador['nome']}")
        print(f"Username: {utilizador['username']}")
        print(f"Password: {'*' * len(utilizador['password'])}")
        print(f"Tipo: {utilizador['tipo']}")

    print("------------------------------------------")

    pausar()


def editar_utilizador():
    if not utilizadores_db.contar():
        print("\nNão existem utilizadores registados.")
        pausar()
        return

    username = input("\nUsername do utilizador: ").strip()

    utilizador = utilizadores_db.obter(username)

    if not utilizador:
        print("\nUtilizador não encontrado.")
        pausar()
        return

    print("\nPrima ENTER para manter o valor atual.\n")

    novo_nome = input(f"Nome ({utilizador['nome']}): ").strip()

    while True:

        novo_username = input(f"Username ({utilizador['username']}): ").strip()

        if not novo_username:
            break

        if novo_username.lower() != username.lower() and username_existe(novo_username):
            print("Esse username já existe.")
            continue

        break

    nova_password = getpass.getpass("Nova password (ENTER para manter): ").strip()

    novo_tipo = utilizador["tipo"]

    while True:

        print("\nTipo:")
        print("1 - Administrador")
        print("2 - Utilizador")
        print("ENTER - Manter")

        opcao = input("Escolha: ").strip()

        if opcao == "":
            break

        elif opcao == "1":
            novo_tipo = "Administrador"
            break

        elif opcao == "2":
            novo_tipo = "Utilizador"
            break

        else:
            print("Opção inválida.")

    editar(username, novo_nome, novo_username, nova_password, novo_tipo)

    print("\nUtilizador atualizado com sucesso!")

    pausar()


def eliminar_utilizador():
    if not utilizadores_db.contar():
        print("\nNão existem utilizadores registados.")
        pausar()
        return

    username = input("\nUsername do utilizador: ").strip()

    utilizador = utilizadores_db.obter(username)

    if not utilizador:
        print("\nUtilizador não encontrado.")
        pausar()
        return

    print("\n========== UTILIZADOR ==========")
    print(f"Nome: {utilizador['nome']}")
    print(f"Username: {utilizador['username']}")
    print(f"Tipo: {utilizador['tipo']}")

    confirmar = input(
        "\nTem a certeza que pretende eliminar este utilizador? (S/N): "
    ).strip().upper()

    if confirmar == "S":
        eliminar(username)
        print("\nUtilizador eliminado com sucesso!")
    else:
        print("\nOperação cancelada.")

    pausar()


def estatisticas():
    dados = resumo()

    print("\n========== ESTATÍSTICAS ==========")
    print(f"Total de utilizadores: {dados['total']}")
    print(f"Administradores: {dados['administradores']}")
    print(f"Utilizadores: {dados['utilizadores']}")

    pausar()


def ver_logs():
    linhas = registos.ver()

    if not linhas:
        print("\nAinda não existem logs.")
        pausar()
        return

    print("\n========== LOGS DO SISTEMA ==========\n")
    print("".join(linhas))

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


def executar():
    inicializar()
    menu()


if __name__ == "__main__":
    executar()
