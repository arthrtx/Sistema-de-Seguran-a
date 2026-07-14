import tkinter as tk
from tkinter import messagebox
import autenticacao


# ==========================
# CORES
# ==========================

COR_FUNDO = "#EAEAEA"
COR_AZUL = "#1F3A5F"
COR_SIDEBAR = "#2C3E50"
COR_BOTAO = "#34495E"


# ==========================
# MÓDULOS ADMIN
# ==========================

MODULOS_ADMIN = [
    "Utilizadores",
    "Logs",
    "Backups",
    "Controlo de Acessos"
]



# ==========================
# ABRIR SISTEMA
# ==========================

def abrir(utilizador=None):

    """
    Abre o painel principal.
    Recebe o utilizador autenticado.
    """

    if utilizador is None:

        utilizador = autenticacao.obter_utilizador_atual()



    if utilizador is None:

        import login

        login.abrir()

        return



    # ==========================
    # JANELA PRINCIPAL
    # ==========================

    root = tk.Tk()

    root.title(
        "Sistema de Segurança"
    )

    root.geometry(
        "1200x700"
    )

    root.configure(
        bg=COR_FUNDO
    )



    # ==========================
    # CABEÇALHO
    # ==========================

    header = tk.Frame(

        root,

        bg=COR_AZUL,

        height=60

    )


    header.pack(

        side="top",

        fill="x"

    )


    header.pack_propagate(
        False
    )



    titulo = tk.Label(

        header,

        text="Sistema Integrado de Segurança",

        font=(

            "Segoe UI",

            18,

            "bold"

        ),

        bg=COR_AZUL,

        fg="white"

    )


    titulo.pack(

        side="left",

        padx=20

    )



    lbl_sessao = tk.Label(

        header,

        text=
        f"{utilizador['nome']} "
        f"({utilizador['tipo']})",

        font=(

            "Segoe UI",

            11

        ),

        bg=COR_AZUL,

        fg="white"

    )


    lbl_sessao.pack(

        side="right",

        padx=20

    )



    # ==========================
    # CORPO
    # ==========================

    corpo = tk.Frame(

        root,

        bg=COR_FUNDO

    )


    corpo.pack(

        fill="both",

        expand=True

    )



    # ==========================
    # MENU LATERAL
    # ==========================

    sidebar = tk.Frame(

        corpo,

        bg=COR_SIDEBAR,

        width=250

    )


    sidebar.pack(

        side="left",

        fill="y"

    )


    sidebar.pack_propagate(
        False
    )



    # ==========================
    # CONTAINER DOS MÓDULOS
    # ==========================

    content = tk.Frame(

        corpo,

        bg="#050816"

    )


    content.pack(

        side="left",

        fill="both",

        expand=True

    )



    # ==========================
    # DASHBOARD
    # ==========================

    def dashboard():


        for widget in content.winfo_children():

            widget.destroy()



        titulo = tk.Label(

            content,

            text="◈ DASHBOARD ◈",

            font=(

                "Segoe UI",

                30,

                "bold"

            ),

            bg="#050816",

            fg="#00FFFF"

        )


        titulo.pack(
            pady=50
        )



        estado = tk.Label(

            content,

            text="● SISTEMA ONLINE",

            font=(

                "Segoe UI",

                16,

                "bold"

            ),

            bg="#050816",

            fg="#00FF66"

        )


        estado.pack()



    # ==========================
    # MOSTRAR PÁGINA
    # ==========================

    def mostrar_pagina(nome):


        # limpar conteúdo

        for widget in content.winfo_children():

            widget.destroy()



        # ======================
        # UTILIZADORES
        # ======================

        if nome == "Utilizadores":

            import inter_utilizadores


            inter_utilizadores.abrir(
                content
            )


            return



        # ======================
        # CONTROLO ACESSOS
        # ======================

        if nome == "Controlo de Acessos":


            if not autenticacao.validar_acesso(
                "Administrador"
            ):

                messagebox.showerror(

                    "Acesso negado",

                    "Este módulo é reservado a Administradores."

                )

                dashboard()

                return



            import controlo_acessos


            controlo_acessos.abrir(

                content,
                dashboard,
                utilizador

            )


            return



        # ======================
        # LOGS
        # ======================

        if nome == "Logs":


            if not autenticacao.validar_acesso(
                "Administrador"
            ):

                messagebox.showerror(

                    "Acesso negado",

                    "Este módulo é reservado a Administradores."

                )

                dashboard()

                return



            import gestor_logs


            gestor_logs.menu(

                container=content

            )


            return



        # ======================
        # OUTROS MÓDULOS
        # ======================

        if nome in MODULOS_ADMIN:


            if not autenticacao.validar_acesso(
                "Administrador"
            ):

                messagebox.showerror(

                    "Acesso negado",

                    f"O módulo {nome} é reservado a Administradores."

                )


                dashboard()

                return



        titulo = tk.Label(

            content,

            text=nome,

            font=(

                "Segoe UI",

                24,

                "bold"

            ),

            bg="#050816",

            fg="white"

        )


        titulo.pack(
            pady=40
        )



        texto = tk.Label(

            content,

            text=
            f"Área destinada ao módulo {nome}.",

            font=(

                "Segoe UI",

                12

            ),

            bg="#050816",

            fg="white"

        )


        texto.pack()



    # ==========================
    # BOTÕES MENU
    # ==========================

    modulos = [

        "Utilizadores",

        "Logs",

        "Câmaras",

        "Controlo de Acessos",

        "Relatórios",

        "Backups"

    ]



    for modulo in modulos:


        btn = tk.Button(

            sidebar,

            text=modulo,

            font=(

                "Segoe UI",

                11

            ),

            bg=COR_BOTAO,

            fg="white",

            activebackground="#5DADE2",

            relief="flat",

            padx=10,

            pady=10,

            command=lambda m=modulo:
            mostrar_pagina(m)

        )


        btn.pack(

            fill="x",

            padx=10,

            pady=4

        )



    # ==========================
    # TERMINAR SESSÃO
    # ==========================

    def terminar_sessao():


        autenticacao.terminar_sessao()


        root.destroy()


        import login

        login.abrir()



    btn_logout = tk.Button(

        sidebar,

        text="Terminar Sessão",

        font=(

            "Segoe UI",

            11,

            "bold"

        ),

        bg="#C0392B",

        fg="white",

        activebackground="#E74C3C",

        relief="flat",

        padx=10,

        pady=10,

        command=terminar_sessao

    )


    btn_logout.pack(

        side="bottom",

        fill="x",

        padx=10,

        pady=10

    )



    # ==========================
    # BARRA ESTADO
    # ==========================

    status = tk.Label(

        root,

        text=
        f"Estado: Sessão iniciada como "
        f"{utilizador['username']} "
        f"({utilizador['tipo']})",

        bd=1,

        relief="sunken",

        anchor="w",

        bg="#D5DBDB"

    )


    status.pack(

        side="bottom",

        fill="x"

    )



    # Página inicial

    dashboard()



    root.mainloop()



# ==========================
# TESTE
# ==========================

if __name__ == "__main__":

    abrir()