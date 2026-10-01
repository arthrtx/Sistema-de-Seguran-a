"""Criação e atualização do esquema da base de dados."""

TABELAS = (
    """
    CREATE TABLE IF NOT EXISTS utilizadores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        tipo TEXT DEFAULT 'Utilizador',
        foto TEXT,
        criado_em TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS acessos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        utilizador TEXT,
        estado TEXT,
        data TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS logs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        modulo TEXT,
        tipo_evento TEXT,
        descricao TEXT,
        nivel TEXT DEFAULT 'INFO',
        data_hora TEXT
    )
    """,
)

# colunas que podem ter sido criadas depois da primeira versão
COLUNAS_NOVAS = {
    "utilizadores": {
        "tipo": "TEXT DEFAULT 'Utilizador'",
        "foto": "TEXT",
        "criado_em": "TEXT",
    },
}


def criar_tabelas(conn):
    """Cria as tabelas em falta e repõe colunas de versões anteriores."""
    cursor = conn.cursor()

    _descartar_esquema_antigo(cursor)

    for sql in TABELAS:
        cursor.execute(sql)

    for tabela, colunas in COLUNAS_NOVAS.items():
        for coluna, definicao in colunas.items():
            _garantir_coluna(cursor, tabela, coluna, definicao)

    conn.commit()


def colunas(cursor, tabela):
    """Devolve os nomes das colunas de uma tabela."""
    return [linha["name"] for linha in cursor.execute(f"PRAGMA table_info({tabela})")]


def _garantir_coluna(cursor, tabela, coluna, definicao):
    if coluna not in colunas(cursor, tabela):
        cursor.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}")


def _descartar_esquema_antigo(cursor):
    """A primeira versão da tabela utilizadores só tinha nome e permissao."""
    existentes = colunas(cursor, "utilizadores")

    if not existentes or "username" in existentes:
        return

    if cursor.execute("SELECT COUNT(*) FROM utilizadores").fetchone()[0]:
        cursor.execute("ALTER TABLE utilizadores RENAME TO utilizadores_antigos")
    else:
        cursor.execute("DROP TABLE utilizadores")
