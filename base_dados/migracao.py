"""Importação dos ficheiros JSON que eram usados antes do SQLite."""

import json

from modulos.config import ARQUIVO, ARQUIVO_ACESSOS

from base_dados import acessos_db, utilizadores_db

SUFIXO = ".migrado"


def migrar():
    """Importa os JSON uma única vez, renomeando-os para .migrado."""
    _migrar_utilizadores()
    _migrar_acessos()


def _migrar_utilizadores():
    if not ARQUIVO.exists():
        return

    for utilizador in _ler(ARQUIVO):
        username = utilizador.get("username", "")

        if not username or utilizadores_db.existe(username):
            continue

        utilizadores_db.criar(
            utilizador.get("nome", username),
            username,
            utilizador.get("password", ""),
            utilizador.get("tipo", "Utilizador"),
            utilizador.get("foto")
        )

    _arquivar(ARQUIVO)


def _migrar_acessos():
    if not ARQUIVO_ACESSOS.exists():
        return

    for evento in _ler(ARQUIVO_ACESSOS):
        acessos_db.registar(
            evento.get("utilizador", ""),
            evento.get("estado", ""),
            evento.get("data")
        )

    _arquivar(ARQUIVO_ACESSOS)


def _ler(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as ficheiro:
            return json.load(ficheiro)
    except Exception as erro:
        print(f"Erro ao ler {caminho}: {erro}")
        return []


def _arquivar(caminho):
    caminho.rename(caminho.with_name(caminho.name + SUFIXO))
