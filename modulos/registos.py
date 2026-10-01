"""Registo de eventos do sistema (ficheiro de log + base de dados)."""

import os
from datetime import datetime

from modulos.config import ARQUIVO_LOG

from base_dados import logs_db

FORMATO_DATA = "%d/%m/%Y %H:%M:%S"


def escrever(evento, modulo="SISTEMA", tipo_evento="SISTEMA", nivel="INFO"):
    """Guarda o evento no ficheiro de log e na tabela de logs."""
    _guardar_no_ficheiro(evento)

    try:
        logs_db.registar(modulo, tipo_evento, evento, nivel)
    except Exception as erro:
        print(f"Erro ao gravar log na base de dados: {erro}")


def ver():
    """Devolve as linhas do ficheiro de log do sistema."""
    if not ARQUIVO_LOG.exists():
        return []

    with open(ARQUIVO_LOG, "r", encoding="utf-8") as ficheiro:
        return ficheiro.readlines()


def _guardar_no_ficheiro(evento):
    try:
        os.makedirs(str(ARQUIVO_LOG.parent), exist_ok=True)

        with open(ARQUIVO_LOG, "a", encoding="utf-8") as ficheiro:
            data = datetime.now().strftime(FORMATO_DATA)

            ficheiro.write(f"{data} - {evento}\n")
    except Exception as erro:
        print(f"Erro ao escrever log: {erro}")
