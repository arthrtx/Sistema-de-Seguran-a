import tkinter as tk
from tkinter import messagebox

from modulos import autenticacao


COR_FUNDO = "#EAEAEA"
COR_AZUL = "#1F3A5F"
COR_SIDEBAR = "#2C3E50"
COR_BOTAO = "#34495E"


MODULOS_ADMIN = ["Utilizadores", "Logs", "Backups", "Controlo de Acessos"]



def abrir(utilizador=None):

    """
    Abre o painel principal.
    Recebe o utilizador autenticado.
    """

    if utilizador is None:

        utilizador = autenticacao.obter_utilizador_atual()



    if utilizador is None:

        from interface_grafica import login

        login.abrir()

        return



    root = tk.Tk()

    root.title("Security System")

    root.geometry("1200x700")

    root.configure(bg=COR_FUNDO)



    header = tk.Frame(root, bg=COR_AZUL, height=60)


    header.pack(side="top", fill="x")


    header.pack_propagate(False)



    titulo = tk.Label(
        header,
        text="Integrated Security System",
        font=("Segoe UI", 18, "bold"),
        bg=COR_AZUL,
        fg="white"
    )


    titulo.pack(side="left", padx=20)



    lbl_sessao = tk.Label(
        header,
        text=f"{utilizador['nome']} ({utilizador['tipo']})",
        font=("Segoe UI", 11),
        bg=COR_AZUL,
        fg="white"
    )


    lbl_sessao.pack(side="right", padx=20)



    corpo = tk.Frame(root, bg=COR_FUNDO)


    corpo.pack(fill="both", expand=True)



    sidebar = tk.Frame(corpo, bg=COR_SIDEBAR, width=250)


    sidebar.pack(side="left", fill="y")


    sidebar.pack_propagate(False)



    content = tk.Frame(corpo, bg="#050816")


    content.pack(side="left", fill="both", expand=True)



    def dashboard():


        for widget in content.winfo_children():

            widget.destroy()



        titulo = tk.Label(
            content,
            text="◈ DASHBOARD ◈",
            font=("Segoe UI", 30, "bold"),
            bg="#050816",
            fg="#00FFFF"
        )


        titulo.pack(pady=50)



        estado = tk.Label(
            content,
            text="● SISTEMA ONLINE",
            font=("Segoe UI", 16, "bold"),
            bg="#050816",
            fg="#00FF66"
        )


        estado.pack()



    def mostrar_pagina(nome):


        # limpar conteúdo

        for widget in content.winfo_children():

            widget.destroy()



        if nome == "Utilizadores":

            from interface_grafica import inter_utilizadores


            inter_utilizadores.abrir(content)


            return



        if nome == "Controlo de Acessos":


            if not autenticacao.validar_acesso("Administrador"):

                messagebox.showerror("Acesso negado", "Este módulo é reservado a Administradores.")

                dashboard()

                return



            from interface_grafica import controlo_acessos


            controlo_acessos.abrir(content, dashboard, utilizador)


            return



        if nome == "Logs":


            if not autenticacao.validar_acesso("Administrador"):

                messagebox.showerror("Acesso negado", "Este módulo é reservado a Administradores.")

                dashboard()

                return



            from interface_grafica import gestor_logs


            gestor_logs.menu(container=content)


            return



        if nome in MODULOS_ADMIN:


            if not autenticacao.validar_acesso("Administrador"):

                messagebox.showerror(
                    "Acesso negado",
                    f"O módulo {nome} é reservado a Administradores."
                )


                dashboard()

                return



        titulo = tk.Label(
            content,
            text=nome,
            font=("Segoe UI", 24, "bold"),
            bg="#050816",
            fg="white"
        )


        titulo.pack(pady=40)



        texto = tk.Label(
            content,
            text=f"Área destinada ao módulo {nome}.",
            font=("Segoe UI", 12),
            bg="#050816",
            fg="white"
        )


        texto.pack()



    modulos = ["Utilizadores", "Logs", "Câmaras", "Controlo de Acessos", "Relatórios", "Backups"]



    for modulo in modulos:


        btn = tk.Button(
            sidebar,
            text=modulo,
            font=("Segoe UI", 11),
            bg=COR_BOTAO,
            fg="white",
            activebackground="#5DADE2",
            relief="flat",
            padx=10,
            pady=10,
            command=lambda m=modulo: mostrar_pagina(m)
        )


        btn.pack(fill="x", padx=10, pady=4)



    def terminar_sessao():


        autenticacao.terminar_sessao()


        root.destroy()


        from interface_grafica import login

        login.abrir()



    btn_logout = tk.Button(
        sidebar,
        text="Terminar Sessão",
        font=("Segoe UI", 11, "bold"),
        bg="#C0392B",
        fg="white",
        activebackground="#E74C3C",
        relief="flat",
        padx=10,
        pady=10,
        command=terminar_sessao
    )


    btn_logout.pack(side="bottom", fill="x", padx=10, pady=10)



    status = tk.Label(
        root,
        text=f"Estado: Sessão iniciada como {utilizador['username']} ({utilizador['tipo']})",
        bd=1,
        relief="sunken",
        anchor="w",
        bg="#D5DBDB"
    )


    status.pack(side="bottom", fill="x")



    # Página inicial

    dashboard()



    root.mainloop()



if __name__ == "__main__":

    abrir()