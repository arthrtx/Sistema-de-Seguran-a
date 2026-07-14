import sqlite3
import os



# ==========================
# FICHEIRO BASE DE DADOS
# ==========================

NOME_BD = "sistema_seguranca.db"



# ==========================
# LIGAÇÃO
# ==========================

def ligar():

    return sqlite3.connect(
        NOME_BD
    )



# ==========================
# CRIAR TABELAS
# ==========================

def criar_tabelas():

    conn = ligar()

    cursor = conn.cursor()



    # ======================
    # UTILIZADORES
    # ======================

    cursor.execute(

        """

        CREATE TABLE IF NOT EXISTS utilizadores(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nome TEXT UNIQUE NOT NULL,

            permissao TEXT DEFAULT 'UTILIZADOR'

        )

        """

    )



    # ======================
    # ACESSOS
    # ======================

    cursor.execute(

        """

        CREATE TABLE IF NOT EXISTS acessos(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            utilizador TEXT,

            estado TEXT,

            data TEXT

        )

        """

    )



    # ======================
    # CORREÇÃO DE BASE ANTIGA
    # ======================

    cursor.execute(

        """

        PRAGMA table_info(utilizadores)

        """

    )



    colunas = [

        coluna[1]

        for coluna in cursor.fetchall()

    ]



    if "permissao" not in colunas:


        cursor.execute(

            """

            ALTER TABLE utilizadores

            ADD COLUMN permissao TEXT DEFAULT 'UTILIZADOR'

            """

        )



    conn.commit()

    conn.close()



# ==========================
# CRIAR ADMIN INICIAL
# ==========================

def criar_admin_inicial(nome="Administrador"):


    conn = ligar()

    cursor = conn.cursor()



    cursor.execute(

        """

        SELECT *

        FROM utilizadores

        WHERE nome=?

        """,

        (
            nome,
        )

    )



    existe = cursor.fetchone()



    if existe is None:


        cursor.execute(

            """

            INSERT INTO utilizadores

            (
                nome,
                permissao
            )

            VALUES(?,?)

            """,

            (

                nome,

                "ADMIN"

            )

        )



    conn.commit()

    conn.close()



# ==========================
# TESTE
# ==========================

if __name__ == "__main__":


    criar_tabelas()

    criar_admin_inicial()


    print(
        "Base de dados criada."
    )