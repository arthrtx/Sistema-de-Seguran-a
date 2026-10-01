import tkinter as tk
from tkinter import messagebox, simpledialog

from modulos import utilizadores
from modulos.Camara import tirarFoto

# Código necessário para criar Administradores
CODIGO_ADMIN = "admin"

COR_FUNDO = "#ECEFF4"
COR_AZUL = "#1F3A5F"
COR_BOTAO = "#2980B9"


def criar():

    nome = entry_nome.get().strip()
    username = entry_user.get().strip()
    password = entry_pass.get().strip()
    tipo = tipo_var.get()

    if nome == "" or username == "" or password == "":
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    if utilizadores.username_existe(username):
        messagebox.showerror("Erro", "Esse username já existe.")
        return

    # Se for administrador pede o código
    if tipo == "Administrador":

        codigo = simpledialog.askstring("Código de Administrador", "Introduza o código:", show="*")

        if codigo != CODIGO_ADMIN:
            messagebox.showerror("Erro", "Código de administrador inválido.")
            return

    messagebox.showinfo("Face ID", "Clique em OK para abrir a câmara.")

    caminho_foto = tirarFoto(username)

    utilizadores.criar(nome, username, password, tipo, caminho_foto)

    messagebox.showinfo("Sucesso", "Conta criada com sucesso!")

    janela.destroy()


def abrir():

    global janela
    global entry_nome
    global entry_user
    global entry_pass
    global tipo_var

    janela = tk.Tk()

    janela.title("Criar Conta")
    janela.geometry("500x550")
    janela.configure(bg=COR_FUNDO)

    tk.Label(janela, text="CRIAR CONTA", font=("Segoe UI", 20, "bold"), bg=COR_FUNDO).pack(pady=20)

    tk.Label(janela, text="Nome", bg=COR_FUNDO).pack()

    entry_nome = tk.Entry(janela, font=("Segoe UI", 12))
    entry_nome.pack(fill="x", padx=40, pady=5)

    tk.Label(janela, text="Username", bg=COR_FUNDO).pack()

    entry_user = tk.Entry(janela, font=("Segoe UI", 12))
    entry_user.pack(fill="x", padx=40, pady=5)

    tk.Label(janela, text="Password", bg=COR_FUNDO).pack()

    entry_pass = tk.Entry(janela, show="*", font=("Segoe UI", 12))
    entry_pass.pack(fill="x", padx=40, pady=5)

    # Tipo de conta
    tk.Label(janela, text="Tipo", bg=COR_FUNDO).pack(pady=10)

    tipo_var = tk.StringVar(value="Utilizador")

    tk.Radiobutton(
        janela,
        text="Administrador",
        variable=tipo_var,
        value="Administrador",
        bg=COR_FUNDO
    ).pack()

    tk.Radiobutton(
        janela,
        text="Utilizador",
        variable=tipo_var,
        value="Utilizador",
        bg=COR_FUNDO
    ).pack()

    tk.Button(
        janela,
        text="Criar Conta",
        bg=COR_BOTAO,
        fg="white",
        font=("Segoe UI", 12, "bold"),
        command=criar
    ).pack(pady=30)

    janela.mainloop()


if __name__ == "__main__":
    abrir()