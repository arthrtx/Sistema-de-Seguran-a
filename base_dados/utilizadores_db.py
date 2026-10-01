"""Acesso à tabela de utilizadores."""

from datetime import datetime

from base_dados import conexao

CAMPOS_EDITAVEIS = ("nome", "username", "password", "tipo", "foto")

FORMATO_DATA = "%Y-%m-%d %H:%M:%S"


def listar():
    """Devolve todos os utilizadores por ordem de nome."""
    conn = conexao.ligar()

    try:
        linhas = conn.execute("SELECT * FROM utilizadores ORDER BY nome COLLATE NOCASE")

        return [dict(linha) for linha in linhas]
    finally:
        conn.close()


def obter(username):
    """Devolve um utilizador pelo username (sem diferenciar maiúsculas)."""
    conn = conexao.ligar()

    try:
        linha = conn.execute(
            "SELECT * FROM utilizadores WHERE username = ? COLLATE NOCASE",
            (username,)
        ).fetchone()

        return dict(linha) if linha else None
    finally:
        conn.close()


def obter_por_id(id_utilizador):
    """Devolve um utilizador pelo id."""
    conn = conexao.ligar()

    try:
        linha = conn.execute("SELECT * FROM utilizadores WHERE id = ?", (id_utilizador,)).fetchone()

        return dict(linha) if linha else None
    finally:
        conn.close()


def existe(username):
    return obter(username) is not None


def criar(nome, username, password, tipo="Utilizador", foto=None):
    """Insere um utilizador e devolve o id atribuído."""
    conn = conexao.ligar()

    try:
        cursor = conn.execute(
            """
            INSERT INTO utilizadores
            (
                nome,
                username,
                password,
                tipo,
                foto,
                criado_em
            )
            VALUES(?,?,?,?,?,?)
            """,
            (nome, username, password, tipo, foto, datetime.now().strftime(FORMATO_DATA))
        )

        conn.commit()

        return cursor.lastrowid
    finally:
        conn.close()


def atualizar(username, campos):
    """Atualiza apenas as colunas indicadas. Devolve True se algo mudou."""
    valores = {campo: valor for campo, valor in campos.items() if campo in CAMPOS_EDITAVEIS and valor}

    if not valores:
        return False

    atribuicoes = ", ".join(f"{campo} = ?" for campo in valores)

    conn = conexao.ligar()

    try:
        cursor = conn.execute(
            f"UPDATE utilizadores SET {atribuicoes} WHERE username = ? COLLATE NOCASE",
            (*valores.values(), username)
        )

        conn.commit()

        return cursor.rowcount > 0
    finally:
        conn.close()


def eliminar(username):
    conn = conexao.ligar()

    try:
        cursor = conn.execute("DELETE FROM utilizadores WHERE username = ? COLLATE NOCASE", (username,))

        conn.commit()

        return cursor.rowcount > 0
    finally:
        conn.close()


def contar():
    conn = conexao.ligar()

    try:
        return conn.execute("SELECT COUNT(*) FROM utilizadores").fetchone()[0]
    finally:
        conn.close()
