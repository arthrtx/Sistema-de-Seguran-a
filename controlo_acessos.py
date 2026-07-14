import tkinter as tk
from tkinter import messagebox
import time
import os

import acessos



# ==========================
# CORES
# ==========================

COR_FUNDO = "#050816"
COR_AZUL = "#00FFFF"
COR_VERDE = "#00FF66"
COR_PAINEL = "#10182B"



# ==========================
# ABRIR MÓDULO
# ==========================

def abrir(container, voltar, utilizador):


    acessos.inicializar()



    # Limpar área principal

    for widget in container.winfo_children():

        widget.destroy()



    container.configure(
        bg=COR_FUNDO
    )



    # ==========================
    # TÍTULO
    # ==========================

    titulo = tk.Label(

        container,

        text="◈ CYBER ACCESS CONTROL ◈",

        bg=COR_FUNDO,

        fg=COR_AZUL,

        font=(
            "Segoe UI",
            30,
            "bold"
        )

    )


    titulo.pack(
        pady=30
    )



    # ==========================
    # ESTADO
    # ==========================

    estado = tk.Label(

        container,

        text=f"● SISTEMA ONLINE | {utilizador['nome']}",

        bg=COR_FUNDO,

        fg=COR_VERDE,

        font=(
            "Segoe UI",
            14,
            "bold"
        )

    )


    estado.pack()



    # ==========================
    # RELÓGIO
    # ==========================

    relogio = tk.Label(

        container,

        bg=COR_FUNDO,

        fg="white",

        font=(
            "Segoe UI",
            14
        )

    )


    relogio.pack(
        pady=10
    )



    def atualizar_relogio():


        relogio.config(

            text="🕒 "
            +
            time.strftime(
                "%d/%m/%Y %H:%M:%S"
            )

        )


        container.after(
            1000,
            atualizar_relogio
        )



    atualizar_relogio()



    # ==========================
    # SCANNER ANIMADO
    # ==========================

    scanner = tk.Label(

        container,

        bg=COR_FUNDO,

        fg=COR_AZUL,

        font=(
            "Segoe UI",
            14,
            "bold"
        )

    )


    scanner.pack()



    simbolos = [

        "▰",

        "▰▰",

        "▰▰▰",

        "▰▰▰▰",

        "▰▰▰▰▰"

    ]


    indice_scanner = 0



    def atualizar_scanner():

        nonlocal indice_scanner


        scanner.config(

            text=
            "SCANNING ACCESS "
            +
            simbolos[indice_scanner]

        )


        indice_scanner = (

            indice_scanner + 1

        ) % len(simbolos)



        container.after(

            300,

            atualizar_scanner

        )



    atualizar_scanner()



    # ==========================
    # LOGS
    # ==========================

    def abrir_logs():


        janela = tk.Toplevel(container)


        janela.title(
            "📄 Logs do Sistema"
        )


        janela.geometry(
            "800x500"
        )


        janela.configure(
            bg=COR_FUNDO
        )



        texto = tk.Text(

            janela,

            bg=COR_PAINEL,

            fg="white",

            font=(
                "Consolas",
                12
            )

        )


        texto.pack(

            expand=True,

            fill="both"

        )



        caminho = (
            "C:/Temp/MinhaPasta/logs.txt"
        )



        if os.path.exists(caminho):


            with open(

                caminho,

                encoding="utf-8"

            ) as ficheiro:


                texto.insert(

                    tk.END,

                    ficheiro.read()

                )


        else:


            texto.insert(

                tk.END,

                "Sem logs."

            )



    # ==========================
    # HISTÓRICO DO UTILIZADOR
    # ==========================

    def abrir_historico():


        try:


            username = utilizador["username"]



            dados = acessos.listar_historico_utilizador(

                username

            )



            texto = ""



            for item in dados:


                texto += (

                    f"Estado: {item['estado']}\n"

                    f"Data: {item['data']}\n"

                    "------------------------\n"

                )



            if texto == "":


                texto = "Sem histórico."



        except Exception as erro:


            texto = (

                "Erro:\n"

                +

                str(erro)

            )



        messagebox.showinfo(

            "📋 Meu Histórico",

            texto

        )



    # ==========================
    # ESTATÍSTICAS
    # ==========================

    def abrir_estatisticas():


        try:


            dados = acessos.obter_estatisticas()



            texto = (

                "📊 ESTATÍSTICAS\n\n"

                f"👤 Utilizadores: "
                f"{dados['utilizadores']}\n\n"

                f"✅ Autorizados: "
                f"{dados['autorizados']}\n\n"

                f"❌ Negados: "
                f"{dados['negados']}\n\n"

                f"🔐 Total Registos: "
                f"{dados['total']}"

            )



        except Exception as erro:


            texto = (

                "Erro ao carregar estatísticas:\n\n"

                +

                str(erro)

            )



        messagebox.showinfo(

            "📊 Estatísticas",

            texto

        )
    # ==========================
    # PERMISSÕES
    # ==========================

    def abrir_permissoes():


        janela_perm = tk.Toplevel(container)


        janela_perm.title(
            "🔐 Gestão de Permissões"
        )


        janela_perm.geometry(
            "750x550"
        )


        janela_perm.configure(
            bg=COR_FUNDO
        )



        titulo_perm = tk.Label(

            janela_perm,

            text="🔐 GESTÃO DE ADMINISTRADORES",

            bg=COR_FUNDO,

            fg=COR_AZUL,

            font=(
                "Segoe UI",
                24,
                "bold"
            )

        )


        titulo_perm.pack(
            pady=25
        )



        lista = tk.Listbox(

            janela_perm,

            width=60,

            height=15,

            bg=COR_PAINEL,

            fg="white",

            font=(
                "Segoe UI",
                13
            ),

            selectbackground="#00BFFF"

        )


        lista.pack(
            pady=20
        )



        dados = []



        def carregar_lista():


            lista.delete(
                0,
                tk.END
            )


            dados.clear()


            try:


                dados.extend(

                    acessos.listar_permissoes()

                )



                for u in dados:


                    lista.insert(

                        tk.END,

                        f"👤 {u['nome']}  |  "
                        f"{u['permissao']}"

                    )



            except Exception as erro:


                lista.insert(

                    tk.END,

                    "Erro: "
                    +
                    str(erro)

                )



        carregar_lista()



        # ==========================
        # ALTERAR ADMIN
        # ==========================

        def alterar_admin():


            selecionado = lista.curselection()



            if not selecionado:


                messagebox.showwarning(

                    "Aviso",

                    "Selecione um utilizador."

                )

                return



            utilizador = dados[

                selecionado[0]

            ]



            resposta = messagebox.askyesno(

                "Confirmar",

                f"Alterar permissões de:\n\n"
                f"{utilizador['nome']}?"

            )



            if resposta:


                resultado = acessos.alterar_permissao(

                    utilizador["username"]

                )



                messagebox.showinfo(

                    "Permissões",

                    resultado

                )



                carregar_lista()



        btn_admin = tk.Button(

            janela_perm,

            text="🔐 ALTERAR ADMIN",

            command=alterar_admin,

            width=30,

            height=2,

            bg="#09243A",

            fg="white",

            font=(
                "Segoe UI",
                12,
                "bold"
            )

        )


        btn_admin.pack(
            pady=10
        )



        btn_fechar = tk.Button(

            janela_perm,

            text="⬅ VOLTAR",

            command=janela_perm.destroy,

            width=30,

            height=2,

            bg="#34495E",

            fg="white",

            font=(
                "Segoe UI",
                12,
                "bold"
            )

        )


        btn_fechar.pack(
            pady=5
        )



    # ==========================
    # PAINEL PRINCIPAL
    # ==========================

    painel = tk.Frame(

        container,

        bg=COR_PAINEL,

        bd=3,

        relief="ridge"

    )


    painel.pack(

        pady=35,

        ipadx=50,

        ipady=20

    )



    estilo_botao = {


        "width":35,

        "height":2,

        "bg":"#09243A",

        "fg":"white",

        "font":(
            "Segoe UI",
            14,
            "bold"
        ),

        "cursor":"hand2"

    }



    tk.Button(

        painel,

        text="📄 LOGS DO SISTEMA",

        command=abrir_logs,

        **estilo_botao

    ).pack(
        pady=8
    )



    tk.Button(

        painel,

        text="📋 MEU HISTÓRICO",

        command=abrir_historico,

        **estilo_botao

    ).pack(
        pady=8
    )



    tk.Button(

        painel,

        text="📊 ESTATÍSTICAS",

        command=abrir_estatisticas,

        **estilo_botao

    ).pack(
        pady=8
    )



    # Apenas administradores

    if utilizador.get("tipo") == "Administrador":


        tk.Button(

            painel,

            text="🔐 PERMISSÕES",

            command=abrir_permissoes,

            **estilo_botao

        ).pack(

            pady=8

        )



    # ==========================
    # VOLTAR AO MENU
    # ==========================

    tk.Button(

        container,

        text="⬅ VOLTAR AO MENU",

        command=voltar,

        width=35,

        height=2,

        bg="#34495E",

        fg="white",

        font=(
            "Segoe UI",
            13,
            "bold"
        )

    ).pack(

        pady=15

    )