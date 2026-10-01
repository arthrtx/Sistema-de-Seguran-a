import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from modulos import autenticacao, registos, utilizadores

COR_FUNDO = "#ECF0F1"
COR_AZUL = "#1F3A5F"
COR_BOTAO = "#34495E"


def abrir(container):

    # Limpar área de conteúdo
    for widget in container.winfo_children():
        widget.destroy()

    principal = tk.Frame(container, bg=COR_FUNDO)

    principal.pack(fill="both", expand=True)

    header = tk.Frame(principal, bg=COR_AZUL, height=60)

    header.pack(fill="x")
    header.pack_propagate(False)

    tk.Label(
        header,
        text="Gestão de Utilizadores",
        bg=COR_AZUL,
        fg="white",
        font=("Segoe UI", 18, "bold")
    ).pack(expand=True)

    frame_tabela = tk.Frame(principal, bg=COR_FUNDO)

    frame_tabela.pack(fill="both", expand=True, padx=15, pady=15)

    colunas = ("id", "nome", "username", "tipo")

    tabela = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=16)

    tabela.heading("id", text="ID")
    tabela.heading("nome", text="Nome")
    tabela.heading("username", text="Username")
    tabela.heading("tipo", text="Tipo")

    tabela.column("id", width=60, anchor="center", stretch=False)

    tabela.column("nome", width=280)

    tabela.column("username", width=220)

    tabela.column("tipo", width=150, anchor="center")

    scroll = ttk.Scrollbar(frame_tabela, orient="vertical", command=tabela.yview)

    tabela.configure(yscrollcommand=scroll.set)

    tabela.pack(side="left", fill="both", expand=True)

    scroll.pack(side="right", fill="y")

    def atualizar_tabela():

        tabela.delete(*tabela.get_children())

        for u in utilizadores.listar():

            tabela.insert("", "end", values=(u["id"], u["nome"], u["username"], u["tipo"]))

    def obter_utilizador():

        selecionado = tabela.selection()

        if not selecionado:

            messagebox.showwarning("Aviso", "Selecione um utilizador.")

            return None

        return tabela.item(selecionado[0])["values"]

    def adicionar():

        from interface_grafica import cadastro
        cadastro.abrir()

    def voltar_dashboard():

        for widget in container.winfo_children():
            widget.destroy()

        tk.Label(
            container,
            text="Dashboard",
            bg="white",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=40)

        tk.Label(
            container,
            text="Selecione um módulo no menu lateral.",
            bg="white",
            font=("Segoe UI", 12)
        ).pack()

    def editar():

        selecionado = obter_utilizador()

        if selecionado is None:
            return

        id_utilizador = selecionado[0]

        utilizador = utilizadores.obter_por_id(id_utilizador)

        if utilizador is None:

            messagebox.showerror("Erro", "Utilizador não encontrado.")

            return

        janela = tk.Toplevel(container)

        janela.title("Editar Utilizador")
        janela.geometry("420x330")
        janela.resizable(False, False)

        # Nome

        tk.Label(janela, text="Nome").pack(pady=(15, 0))

        entry_nome = tk.Entry(janela, width=35)

        entry_nome.insert(0, utilizador["nome"])

        entry_nome.pack()

        # Username

        tk.Label(janela, text="Username").pack(pady=(10, 0))

        entry_username = tk.Entry(janela, width=35)

        entry_username.insert(0, utilizador["username"])

        entry_username.pack()

        # Password

        tk.Label(janela, text="Password").pack(pady=(10, 0))

        entry_password = tk.Entry(janela, show="*", width=35)

        entry_password.insert(0, utilizador["password"])

        entry_password.pack()

        # Tipo (não editável)

        tk.Label(
            janela,
            text=f"Tipo: {utilizador['tipo']}",
            font=("Segoe UI", 10, "bold"),
            fg=COR_AZUL
        ).pack(pady=15)

        def guardar():

            nome = entry_nome.get().strip()
            username = entry_username.get().strip()
            password = entry_password.get().strip()

            if nome == "" or username == "" or password == "":

                messagebox.showwarning("Aviso", "Preencha todos os campos.")

                return

            if username.lower() != utilizador["username"].lower() and utilizadores.username_existe(username):

                messagebox.showerror("Erro", "Esse username já existe.")

                return

            if utilizadores.editar(utilizador["username"], nome, username, password):

                registos.escrever(f"Utilizador '{utilizador['username']}' editado.")

                atualizar_tabela()

                messagebox.showinfo("Sucesso", "Utilizador atualizado com sucesso.")

            else:

                messagebox.showerror("Erro", "Não foi possível atualizar o utilizador.")

            janela.destroy()

        tk.Button(
            janela,
            text="Guardar",
            width=15,
            bg=COR_BOTAO,
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=guardar
        ).pack(pady=20)

    def eliminar():

        selecionado = obter_utilizador()

        if selecionado is None:
            return
        username = selecionado[2]

        sessao = autenticacao.obter_utilizador_atual()

        if not sessao:

            messagebox.showerror("Erro", "Não existe sessão ativa.")

            return

        senha = simpledialog.askstring(
            "Autenticação",
            "Introduza a palavra-passe do administrador:",
            show="*"
        )

        if senha is None:
            return

        if senha != sessao["password"]:

            messagebox.showerror("Erro", "Palavra-passe incorreta.")

            return

        confirmar = messagebox.askyesno(
            "Confirmação",
            f"Pretende eliminar o utilizador '{username}'?"
        )

        if not confirmar:
            return

        if utilizadores.eliminar(username):

            atualizar_tabela()

            messagebox.showinfo("Sucesso", "Utilizador eliminado com sucesso.")

        else:

            messagebox.showerror("Erro", "Utilizador não encontrado.")

    frame_botoes = tk.Frame(principal, bg=COR_FUNDO)

    frame_botoes.pack(fill="x", pady=(0, 15))

    tk.Button(
        frame_botoes,
        text="Adicionar",
        width=15,
        bg=COR_BOTAO,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=adicionar
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    tk.Button(
        frame_botoes,
        text="Editar",
        width=15,
        bg=COR_BOTAO,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=editar
    ).grid(
        row=0,
        column=1,
        padx=10
    )

    tk.Button(
        frame_botoes,
        text="Eliminar",
        width=15,
        bg="#C0392B",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=eliminar
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    tk.Button(
        frame_botoes,
        text="Atualizar",
        width=15,
        bg=COR_BOTAO,
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=atualizar_tabela
    ).grid(
        row=0,
        column=3,
        padx=10
    )

    tk.Button(
        frame_botoes,
        text="Voltar",
        width=15,
        bg="#7F8C8D",
        fg="white",
        font=("Segoe UI", 11, "bold"),
        command=voltar_dashboard
    ).grid(
        row=0,
        column=4,
        padx=10
    )

    atualizar_tabela()