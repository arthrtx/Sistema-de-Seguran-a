import tkinter as tk
from tkinter import messagebox

from modulos import autenticacao
from interface_grafica import cadastro

COR_FUNDO = "#ECEFF4"
COR_AZUL = "#1F3A5F"
COR_BOTAO = "#2980B9"
COR_BOTAO_HOVER = "#3498DB"


def abrir():

    root = tk.Tk()
    root.title("Integrated Security System")
    root.configure(bg=COR_FUNDO)
    root.resizable(False, False)

    # Centralizar janela

    largura = 900
    altura = 600

    x = (root.winfo_screenwidth() // 2) - (largura // 2)
    y = (root.winfo_screenheight() // 2) - (altura // 2)

    root.geometry(f"{largura}x{altura}+{x}+{y}")

    header = tk.Frame(root, bg=COR_AZUL, height=80)

    header.pack(fill="x")

    titulo = tk.Label(
        header,
        text="Integrated Security System",
        bg=COR_AZUL,
        fg="white",
        font=("Segoe UI", 22, "bold")
    )

    titulo.pack(pady=18)

    card = tk.Frame(root, bg="white", bd=1, relief="solid")

    card.place(relx=0.5, rely=0.55, anchor="center", width=420, height=360)

    titulo_login = tk.Label(card, text="LOGIN", bg="white", font=("Segoe UI", 18, "bold"))

    titulo_login.pack(pady=(25, 20))

    lbl_user = tk.Label(card, text="Utilizador", bg="white", font=("Segoe UI", 11))

    lbl_user.pack(anchor="w", padx=35)

    entry_user = tk.Entry(card, font=("Segoe UI", 12))

    entry_user.pack(padx=35, fill="x", ipady=6, pady=(5, 15))

    lbl_pass = tk.Label(card, text="Palavra-passe", bg="white", font=("Segoe UI", 11))

    lbl_pass.pack(anchor="w", padx=35)

    entry_pass = tk.Entry(card, show="*", font=("Segoe UI", 12))

    entry_pass.pack(padx=35, fill="x", ipady=6, pady=(5, 25))

    def hover(e):
        btn_login["bg"] = COR_BOTAO_HOVER

    def leave(e):
        btn_login["bg"] = COR_BOTAO

    def login():

        username = entry_user.get().strip()
        password = entry_pass.get()

        if username == "" or password == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return

        # Usa o módulo autenticacao.py:
        #   - valida username + password
        #   - bloqueia após demasiadas tentativas
        #   - regista tudo nos logs

        sucesso, mensagem, utilizador = autenticacao.autenticar(username, password)

        if not sucesso:
            messagebox.showerror("Erro", mensagem)
            entry_pass.delete(0, tk.END)
            return

        messagebox.showinfo("Sucesso", mensagem)

        root.destroy()

        # Abrir o painel principal já com a sessão iniciada
        from interface_grafica import interface
        interface.abrir(utilizador)

    def abrir_cadastro():

        root.destroy()
        cadastro.abrir()

    btn_login = tk.Button(
        card,
        text="Entrar",
        bg=COR_BOTAO,
        fg="white",
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 12, "bold"),
        command=login
    )

    btn_login.pack(ipadx=35, ipady=8)

    btn_login.bind("<Enter>", hover)
    btn_login.bind("<Leave>", leave)

    # Permitir fazer login com a tecla ENTER
    root.bind("<Return>", lambda e: login())

    btn_cadastro = tk.Button(
        card,
        text="Criar Conta",
        bg="white",
        fg=COR_AZUL,
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 11, "underline"),
        command=abrir_cadastro
    )

    btn_cadastro.pack(pady=18)

    rodape = tk.Label(
        root,
        text="© 2026 Integrated Security System",
        bg=COR_FUNDO,
        fg="gray",
        font=("Segoe UI", 9)
    )

    rodape.pack(side="bottom", pady=12)

    root.mainloop()


if __name__ == "__main__":
    abrir()
