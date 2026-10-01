"""Acesso à tabela de logs."""

from datetime import datetime

from base_dados import conexao

FORMATO_DATA = "%Y-%m-%d %H:%M:%S"


def registar(modulo, tipo_evento, descricao, nivel="INFO", data_hora=None):
    """Guarda um evento de log."""
    conn = conexao.ligar()

    try:
        conn.execute(
            """
            INSERT INTO logs
            (
                modulo,
                tipo_evento,
                descricao,
                nivel,
                data_hora
            )
            VALUES(?,?,?,?,?)
            """,
            (
                modulo,
                tipo_evento,
                descricao,
                nivel,
                data_hora or datetime.now().strftime(FORMATO_DATA)
            )
        )

        conn.commit()
    finally:
        conn.close()


def listar(limite=500):
    """Devolve os eventos mais recentes."""
    conn = conexao.ligar()

    try:
        linhas = conn.execute("SELECT * FROM logs ORDER BY id DESC LIMIT ?", (limite,))

        return [dict(linha) for linha in linhas]
    finally:
        conn.close()


def listar_por_modulo(modulo, limite=500):
    conn = conexao.ligar()

    try:
        linhas = conn.execute(
            "SELECT * FROM logs WHERE modulo = ? COLLATE NOCASE ORDER BY id DESC LIMIT ?",
            (modulo, limite)
        )

        return [dict(linha) for linha in linhas]
    finally:
        conn.close()


def apagar_por_id(id_log):
    conn = conexao.ligar()

    try:
        cursor = conn.execute("DELETE FROM logs WHERE id = ?", (id_log,))

        conn.commit()

        return cursor.rowcount > 0
    finally:
        conn.close()


def contar():
    conn = conexao.ligar()

    try:
        return conn.execute("SELECT COUNT(*) FROM logs").fetchone()[0]
    finally:
        conn.close()
