import os
import sqlite3
from pathlib import Path

from modulos.config import BD, NOME_BD, PASTA_DADOS

# Migração de bases de dados antigas (nome em português ou ficheiro na raiz do projeto)
_BD_ANTIGA = PASTA_DADOS / "sistema_seguranca.db"
_BD_NA_PROJETO = Path(__file__).resolve().parent.parent / NOME_BD

for _antigo in (_BD_ANTIGA, _BD_NA_PROJETO):
    if not BD.exists() and _antigo.exists():
        os.replace(_antigo, BD)

_esquema_pronto = False


def ligar():
    """Abre a base de dados. O esquema é criado na primeira ligação."""
    global _esquema_pronto

    # import tardio evita ciclo entre o pacote e o esquema
    from base_dados import esquema

    conn = sqlite3.connect(str(BD))

    conn.row_factory = sqlite3.Row

    if not _esquema_pronto:
        esquema.criar_tabelas(conn)
        _esquema_pronto = True

    return conn
