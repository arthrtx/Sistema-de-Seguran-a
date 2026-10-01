"""
Camada 3 - persistência dos dados em SQLite.

    base_dados.conexao         -> ligação à base de dados
    base_dados.esquema         -> criação e atualização das tabelas
    base_dados.utilizadores_db -> tabela de utilizadores
    base_dados.acessos_db      -> tabela de acessos
    base_dados.logs_db         -> tabela de logs
    base_dados.migracao        -> importação dos ficheiros JSON antigos
"""

from base_dados import conexao
from base_dados import acessos_db, logs_db, utilizadores_db
from base_dados import migracao
from base_dados.conexao import BD, ligar


def inicializar():
    """Garante que o esquema existe e importa os dados antigos."""
    conn = ligar()
    conn.close()

    migracao.migrar()


inicializar()

__all__ = [
    "BD",
    "acessos_db",
    "conexao",
    "inicializar",
    "ligar",
    "logs_db",
    "migracao",
    "utilizadores_db",
]
