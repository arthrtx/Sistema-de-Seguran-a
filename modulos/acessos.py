import logging
from datetime import datetime

from modulos.config import ARQUIVO_LOG

from base_dados import acessos_db, utilizadores_db

FORMATO_DATA = "%d/%m/%Y %H:%M:%S"

logging.basicConfig(
    filename=str(ARQUIVO_LOG),
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)


def data_atual():
    return datetime.now().strftime(FORMATO_DATA)


def listar_permissoes():
    """Devolve nome, username e permissão de cada utilizador."""
    return [
        {
            "nome": utilizador["nome"],
            "username": utilizador["username"],
            "permissao": utilizador["tipo"]
        }
        for utilizador in utilizadores_db.listar()
    ]


def alterar_permissao(username):
    """Alterna entre Administrador e Utilizador."""
    utilizador = utilizadores_db.obter(username)

    if not utilizador:
        return "Utilizador não encontrado"

    novo_tipo = "Utilizador" if utilizador["tipo"] == "Administrador" else "Administrador"

    utilizadores_db.atualizar(username, {"tipo": novo_tipo})

    logging.info(f"Permissão alterada: {username}")

    return f"{username} agora é {novo_tipo}"


def registar_evento(utilizador, estado):
    acessos_db.registar(utilizador, estado, data_atual())


def registar_login(username):
    registar_evento(username, "LOGIN")


def registar_logout(username):
    registar_evento(username, "LOGOUT")


def registar_permissao(username, estado):
    registar_evento(username, "AUTORIZADO" if estado else "NEGADO")


def listar_historico():
    return acessos_db.listar()


def listar_historico_utilizador(nome):
    return acessos_db.listar_por_utilizador(nome)


def obter_estatisticas():
    return acessos_db.estatisticas()


def inicializar():
    logging.info("Controlo de acessos iniciado")
