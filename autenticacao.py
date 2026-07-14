import json
import os
import getpass

from datetime import datetime, timedelta

import acessos



# =====================================================
# CONFIGURAÇÕES
# =====================================================

ARQUIVO = (
    "C:/Temp/MinhaPasta/utilizadores.txt"
)


ARQUIVO_LOG = (
    "C:/Temp/MinhaPasta/logs.txt"
)



MAX_TENTATIVAS = 3


TEMPO_BLOQUEIO = 60



utilizadores = []


sessao = None



tentativas_falhadas = {}



# =====================================================
# INICIALIZAÇÃO
# =====================================================

def inicializar():

    carregar_utilizadores()

    print(
        "\nMódulo de Autenticação iniciado!"
    )



# =====================================================
# CARREGAR UTILIZADORES
# =====================================================

def carregar_utilizadores():

    global utilizadores



    if not os.path.exists(
        ARQUIVO
    ):

        utilizadores = []

        return



    try:


        with open(

            ARQUIVO,

            "r",

            encoding="utf-8"

        ) as ficheiro:


            utilizadores = json.load(
                ficheiro
            )



    except Exception:


        utilizadores = []



# =====================================================
# LOGS
# =====================================================

def escrever_log(evento):


    try:


        os.makedirs(

            os.path.dirname(
                ARQUIVO_LOG
            ),

            exist_ok=True

        )



        with open(

            ARQUIVO_LOG,

            "a",

            encoding="utf-8"

        ) as ficheiro:



            data = datetime.now().strftime(

                "%d/%m/%Y %H:%M:%S"

            )



            ficheiro.write(

                f"{data} - [AUTENTICACAO] {evento}\n"

            )



    except Exception as erro:


        print(
            "Erro ao escrever log:",
            erro
        )



# =====================================================
# AUXILIARES
# =====================================================

def pausar():

    input(
        "\nPrima ENTER para continuar..."
    )



def procurar_utilizador(username):


    for utilizador in utilizadores:


        if utilizador["username"].lower() == username.lower():


            return utilizador



    return None



# =====================================================
# BLOQUEIO DE LOGIN
# =====================================================

def username_bloqueado(username):


    registo = tentativas_falhadas.get(

        username.lower()

    )



    if not registo:

        return False



    bloqueado = registo.get(

        "bloqueado_ate"

    )



    if not bloqueado:

        return False



    if datetime.now() < bloqueado:


        return True



    tentativas_falhadas[

        username.lower()

    ] = {


        "tentativas":0,


        "bloqueado_ate":None

    }



    return False



def registar_tentativa_falhada(username):


    chave = username.lower()



    registo = tentativas_falhadas.get(

        chave,

        {

            "tentativas":0,

            "bloqueado_ate":None

        }

    )



    registo["tentativas"] += 1



    if registo["tentativas"] >= MAX_TENTATIVAS:


        registo["bloqueado_ate"] = (

            datetime.now()

            +

            timedelta(

                seconds=TEMPO_BLOQUEIO

            )

        )


        registo["tentativas"] = 0



        escrever_log(

            f"Username {username} bloqueado por excesso de tentativas."

        )



    tentativas_falhadas[chave] = registo



def limpar_tentativas(username):


    tentativas_falhadas[

        username.lower()

    ] = {


        "tentativas":0,


        "bloqueado_ate":None

    }

# =====================================================
# LOGIN DIRETO
# =====================================================

def login_direto(username, password):

    global sessao



    utilizador = procurar_utilizador(
        username
    )



    if not utilizador:


        escrever_log(
            f"Login falhado: {username}"
        )


        registar_tentativa_falhada(
            username
        )


        return None



    if utilizador["password"] != password:


        escrever_log(
            f"Password errada: {username}"
        )


        registar_tentativa_falhada(
            username
        )


        return None



    # LOGIN CORRETO

    sessao = utilizador


    limpar_tentativas(
        username
    )



    try:


        acessos.registar_login(

            utilizador["username"]

        )


    except Exception as erro:


        escrever_log(

            f"Erro ao registar login: {erro}"

        )



    escrever_log(

        f"Login efetuado: {utilizador['username']} "

        f"({utilizador.get('tipo','Utilizador')})"

    )



    return utilizador





# =====================================================
# AUTENTICAÇÃO PARA INTERFACE GRÁFICA
# =====================================================

def autenticar(username, password):

    global sessao



    carregar_utilizadores()



    if not utilizadores:


        return (

            False,

            "Não existem utilizadores registados.",

            None

        )



    if username_bloqueado(username):


        registo = tentativas_falhadas.get(

            username.lower()

        )


        segundos = int(

            (

                registo["bloqueado_ate"]

                -

                datetime.now()

            ).total_seconds()

        )



        return (

            False,

            f"Utilizador bloqueado.\n"

            f"Tente novamente em {segundos} segundos.",

            None

        )



    utilizador = procurar_utilizador(

        username

    )



    if (

        not utilizador

        or

        utilizador["password"] != password

    ):



        registar_tentativa_falhada(

            username

        )



        escrever_log(

            f"Login inválido: {username}"

        )



        registo = tentativas_falhadas.get(

            username.lower(),

            {}

        )



        tentativas = registo.get(

            "tentativas",

            0

        )



        restantes = MAX_TENTATIVAS - tentativas



        return (

            False,

            f"Username ou password incorretos.\n"

            f"Tentativas restantes: {restantes}",

            None

        )





    # LOGIN ACEITE


    sessao = utilizador



    limpar_tentativas(

        username

    )



    try:


        acessos.registar_login(

            utilizador["username"]

        )


    except Exception as erro:


        escrever_log(

            f"Erro histórico login: {erro}"

        )



    escrever_log(

        f"Sessão iniciada: "

        f"{utilizador['username']}"

    )



    return (

        True,

        f"Bem-vindo {utilizador['nome']}!",

        utilizador

    )





# =====================================================
# SESSÃO ATUAL
# =====================================================

def sessao_ativa():


    return sessao is not None





def obter_utilizador_atual():


    return sessao





# =====================================================
# TERMINAR SESSÃO
# =====================================================

def terminar_sessao():

    global sessao



    if sessao:



        try:


            acessos.registar_logout(

                sessao["username"]

            )


        except Exception as erro:


            escrever_log(

                f"Erro logout: {erro}"

            )



        escrever_log(

            f"Logout: {sessao['username']}"

        )



        sessao = None

# =====================================================
# PERMISSÕES
# =====================================================

def tem_permissao(tipo_necessario):


    if not sessao:

        return False



    tipo = sessao.get(

        "tipo",

        "Utilizador"

    )



    # Administrador tem acesso total

    if tipo == "Administrador":

        return True



    return tipo == tipo_necessario





def validar_acesso(tipo_necessario="Utilizador"):


    if not sessao:


        escrever_log(

            "Acesso negado: sem sessão ativa."

        )


        return False



    if tem_permissao(tipo_necessario):


        escrever_log(

            f"Acesso autorizado: "

            f"{sessao['username']} "

            f"({tipo_necessario})"

        )


        return True



    escrever_log(

        f"Acesso negado: "

        f"{sessao['username']} "

        f"não possui {tipo_necessario}"

    )



    return False





# =====================================================
# LOGOUT PARA MENU DE CONSOLA
# =====================================================

def logout():


    global sessao



    if not sessao:


        print(

            "\nNão existe sessão ativa."

        )

        pausar()

        return



    username = sessao["username"]



    try:


        acessos.registar_logout(

            username

        )


    except:


        pass



    escrever_log(

        f"Logout: {username}"

    )



    print(

        f"\nSessão terminada: {username}"

    )



    sessao = None



    pausar()





# =====================================================
# ESTADO DA SESSÃO
# =====================================================

def estado_sessao():


    print(

        "\n========== SESSÃO =========="

    )



    if sessao:


        print(

            f"Nome: {sessao['nome']}"

        )


        print(

            f"Username: {sessao['username']}"

        )


        print(

            f"Tipo: {sessao.get('tipo','Utilizador')}"

        )



    else:


        print(

            "Nenhuma sessão ativa."

        )



    pausar()





# =====================================================
# LOGIN MANUAL
# =====================================================

def login():


    global sessao



    carregar_utilizadores()



    print(

        "\n========== LOGIN =========="

    )



    username = input(

        "Username: "

    ).strip()



    password = getpass.getpass(

        "Password: "

    ).strip()



    resultado = login_direto(

        username,

        password

    )



    if resultado:


        print(

            f"\nBem-vindo {resultado['nome']}"

        )


        print(

            f"Tipo: {resultado.get('tipo')}"

        )


    else:


        print(

            "\nCredenciais inválidas."

        )



    pausar()





# =====================================================
# MENU
# =====================================================

def menu():


    while True:


        print(

            """

==============================
        AUTENTICAÇÃO
==============================

1 - Login
2 - Logout
3 - Estado da sessão
4 - Testar acesso Utilizador
5 - Testar acesso Administrador
0 - Sair

==============================
"""

        )



        opcao = input(

            "Escolha: "

        )



        if opcao == "1":


            login()



        elif opcao == "2":


            logout()



        elif opcao == "3":


            estado_sessao()



        elif opcao == "4":


            if validar_acesso(

                "Utilizador"

            ):


                print(

                    "Acesso autorizado."

                )

            else:


                print(

                    "Acesso negado."

                )


            pausar()



        elif opcao == "5":


            if validar_acesso(

                "Administrador"

            ):


                print(

                    "Acesso autorizado."

                )

            else:


                print(

                    "Acesso negado."

                )


            pausar()



        elif opcao == "0":


            break



        else:


            print(

                "Opção inválida."

            )





# =====================================================
# EXECUTOR
# =====================================================

def executar():

    inicializar()

    menu()





if __name__ == "__main__":


    executar()