import json
import os
import logging
from datetime import datetime



# ==========================
# FICHEIROS
# ==========================

ARQUIVO_UTILIZADORES = (
    "C:/Temp/MinhaPasta/utilizadores.txt"
)


ARQUIVO_ACESSOS = (
    "C:/Temp/MinhaPasta/acessos.txt"
)



ARQUIVO_LOG = (
    "C:/Temp/MinhaPasta/logs.txt"
)



# ==========================
# LOG
# ==========================

logging.basicConfig(

    filename=ARQUIVO_LOG,

    level=logging.INFO,

    format="%(asctime)s - %(message)s"

)



# ==========================
# DATA
# ==========================

def data_atual():

    return datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )



# ==========================
# UTILIZADORES
# ==========================

def carregar_utilizadores():

    if not os.path.exists(
        ARQUIVO_UTILIZADORES
    ):

        return []


    try:

        with open(
            ARQUIVO_UTILIZADORES,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    except:

        return []



def guardar_utilizadores(lista):

    with open(
        ARQUIVO_UTILIZADORES,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            lista,
            f,
            indent=4,
            ensure_ascii=False
        )



# ==========================
# PERMISSÕES
# ==========================

def listar_permissoes():

    utilizadores = carregar_utilizadores()


    lista = []


    for u in utilizadores:


        lista.append({

            "nome":
            u["nome"],


            "username":
            u["username"],


            "permissao":
            u.get(
                "tipo",
                "Utilizador"
            )

        })


    return lista



def alterar_permissao(username):


    utilizadores = carregar_utilizadores()



    for u in utilizadores:


        if u["username"] == username:



            if u["tipo"] == "Administrador":

                u["tipo"] = "Utilizador"


            else:

                u["tipo"] = "Administrador"



            guardar_utilizadores(
                utilizadores
            )


            logging.info(
                f"Permissão alterada: {username}"
            )


            return (
                f"{username} agora é {u['tipo']}"
            )



    return "Utilizador não encontrado"



# ==========================
# HISTÓRICO
# ==========================

def guardar_evento(
    utilizador,
    estado
):


    dados = []


    if os.path.exists(
        ARQUIVO_ACESSOS
    ):


        with open(
            ARQUIVO_ACESSOS,
            "r",
            encoding="utf-8"
        ) as f:

            dados = json.load(f)



    dados.append({

        "utilizador":
        utilizador,


        "estado":
        estado,


        "data":
        data_atual()

    })



    with open(
        ARQUIVO_ACESSOS,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(
            dados,
            f,
            indent=4,
            ensure_ascii=False
        )



def registar_login(username):

    guardar_evento(
        username,
        "LOGIN"
    )



def registar_logout(username):

    guardar_evento(
        username,
        "LOGOUT"
    )



# ==========================
# ACESSO
# ==========================

def solicitar_acesso(nome):


    utilizadores = carregar_utilizadores()



    autorizado = False



    for u in utilizadores:


        if u["nome"].lower() == nome.lower():

            autorizado=True



    if autorizado:


        estado="AUTORIZADO"

        resposta="✔ ACESSO AUTORIZADO"


    else:


        estado="NEGADO"

        resposta="✖ ACESSO NEGADO"



    guardar_evento(
        nome,
        estado
    )


    return resposta



# ==========================
# HISTÓRICO
# ==========================

def listar_historico():

    if not os.path.exists(
        ARQUIVO_ACESSOS
    ):

        return []


    with open(
        ARQUIVO_ACESSOS,
        encoding="utf-8"
    ) as f:

        return json.load(f)



def listar_historico_utilizador(nome):


    return [

        h

        for h in listar_historico()

        if h["utilizador"] == nome

    ]



# ==========================
# ESTATÍSTICAS
# ==========================

def obter_estatisticas():


    utilizadores = carregar_utilizadores()

    historico = listar_historico()



    autorizados=0
    negados=0



    for h in historico:


        if h["estado"]=="AUTORIZADO":

            autorizados+=1


        elif h["estado"]=="NEGADO":

            negados+=1



    return {


        "utilizadores":
        len(utilizadores),


        "autorizados":
        autorizados,


        "negados":
        negados,


        "total":
        len(historico)

    }



def inicializar():

    logging.info(
        "Controlo de acessos iniciado"
    )