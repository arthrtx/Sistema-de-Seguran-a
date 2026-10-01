"""Acesso à tabela de acessos."""

from datetime import datetime

from base_dados import conexao, utilizadores_db

FORMATO_DATA = "%d/%m/%Y %H:%M:%S"


def registar(utilizador, estado, data=None):
    """Regista um evento de acesso (LOGIN, LOGOUT, AUTORIZADO, NEGADO)."""
    conn = conexao.ligar()

    try:
        conn.execute(
            "INSERT INTO acessos (utilizador, estado, data) VALUES(?,?,?)",
            (utilizador, estado, data or datetime.now().strftime(FORMATO_DATA))
        )

        conn.commit()
    finally:
        conn.close()


def listar():
    """Devolve o histórico de acessos, do mais recente para o mais antigo."""
    conn = conexao.ligar()

    try:
        linhas = conn.execute("SELECT * FROM acessos ORDER BY id DESC")

        return [dict(linha) for linha in linhas]
    finally:
        conn.close()


def listar_por_utilizador(utilizador):
    conn = conexao.ligar()

    try:
        linhas = conn.execute(
            "SELECT * FROM acessos WHERE utilizador = ? COLLATE NOCASE ORDER BY id DESC",
            (utilizador,)
        )

        return [dict(linha) for linha in linhas]
    finally:
        conn.close()


def estatisticas():
    """Conta os eventos por estado e o total de utilizadores."""
    conn = conexao.ligar()

    try:
        total = conn.execute("SELECT COUNT(*) FROM acessos").fetchone()[0]

        autorizados = conn.execute("SELECT COUNT(*) FROM acessos WHERE estado = 'AUTORIZADO'").fetchone()[0]

        negados = conn.execute("SELECT COUNT(*) FROM acessos WHERE estado = 'NEGADO'").fetchone()[0]
    finally:
        conn.close()

    return {
        "utilizadores": utilizadores_db.contar(),
        "autorizados": autorizados,
        "negados": negados,
        "total": total
    }
