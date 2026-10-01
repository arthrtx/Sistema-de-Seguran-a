import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import tkinter as tk
from tkinter import messagebox, ttk, filedialog

from modulos.config import PASTA_LOGS

from base_dados import logs_db

FORMATO_LOG = "%(asctime)s | %(levelname)s | %(message)s"

logging.basicConfig(level=logging.INFO, format=FORMATO_LOG, handlers=[logging.StreamHandler()])

MODULOS_PERMITIDOS = ["ALARMES", "SENSORES", "CAMARAS", "CONTROLO DE ACESSOS", "RECONHECIMENTO", "RELATORIOS", "BACKUPS", "LOGS"]
NIVEIS_PERMITIDOS = ["INFO", "WARNING", "CRITICAL"]

@dataclass
class RegistoLog:
    id_log: int
    data_hora: datetime
    modulo: str
    tipo_evento: str
    descricao: str
    nivel: str

class GestorLogs:
    def __init__(self):
        self.historico_logs = []
        self.proximo_id = 1
        self._loggers_ativos = {}

    def _validar_texto_puro(self, texto: str) -> bool:
        if not texto or not texto.strip():
            return False
        if texto.strip() in [".", ",", "-", "_", "P", "p"]:
            return False
        return bool(re.match(r"^[A-Za-z0-9 À-ÿ\s\-_:().,!?]+$", texto))

    def _obter_logger_modulo(self, nome_modulo: str):
        nome_modulo = nome_modulo.upper()
        if nome_modulo not in self._loggers_ativos:
            logger = logging.getLogger(nome_modulo)
            logger.setLevel(logging.INFO)
            logger.propagate = True

            nome_ficheiro = nome_modulo.lower().replace(" ", "_")
            caminho_ficheiro = PASTA_LOGS / f"modulo_{nome_ficheiro}.log"

            file_handler = logging.FileHandler(str(caminho_ficheiro), encoding="utf-8")
            file_handler.setFormatter(logging.Formatter(FORMATO_LOG))

            logger.addHandler(file_handler)
            self._loggers_ativos[nome_modulo] = logger

        return self._loggers_ativos[nome_modulo]

    def processar_linha_log(self, linha: str, modulo_padrao: str = "LOGS") -> bool:
        """Faz o parsing de uma linha de log física e adiciona-a à memória RAM."""
        try:
            if " | " not in linha:
                return False

            partes = linha.split(" | ")
            if len(partes) < 3:
                return False

            data_str = partes[0].split(",")[0].strip()
            nivel = partes[1].strip()
            resto = partes[2].strip()

            if resto.startswith("->") and ":" in resto:
                evento_partes = resto.replace("->", "", 1).split(":", 1)
                tipo_evento = evento_partes[0].strip().upper()
                descricao = evento_partes[1].strip()
            else:
                tipo_evento = "SISTEMA"
                descricao = resto

            try:
                dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                dt = datetime.now()

            novo_log = RegistoLog(
                id_log=self.proximo_id,
                data_hora=dt,
                modulo=modulo_padrao.upper(),
                tipo_evento=tipo_evento,
                descricao=descricao,
                nivel=nivel if nivel in NIVEIS_PERMITIDOS else "INFO"
            )
            self.historico_logs.append(novo_log)
            self.proximo_id += 1
            return True
        except Exception:
            return False

    def carregar_de_ficheiro(self, caminho_ficheiro: Path):
        """Lê um ficheiro de log específico e processa todas as linhas."""
        caminho = Path(caminho_ficheiro)
        if not caminho.exists():
            return 0

        nome = caminho.stem.lower()
        modulo_detetado = "LOGS"
        for m in MODULOS_PERMITIDOS:
            if m.lower().replace(" ", "_") in nome:
                modulo_detetado = m
                break

        contador = 0
        with open(caminho, "r", encoding="utf-8") as f:
            for linha in f:
                if self.processar_linha_log(linha, modulo_detetado):
                    contador += 1
        return contador

    def registar(self, modulo: str, tipo_evento: str, descricao: str, nivel: str = "INFO"):
        modulo = str(modulo or "").upper().strip()
        nivel_upper = str(nivel or "").upper().strip()

        if modulo not in MODULOS_PERMITIDOS:
            return False
        if nivel_upper not in NIVEIS_PERMITIDOS:
            nivel_upper = "INFO"
        if not self._validar_texto_puro(tipo_evento) or not self._validar_texto_puro(descricao):
            return False

        novo_log = RegistoLog(
            id_log=self.proximo_id,
            data_hora=datetime.now(),
            modulo=modulo,
            tipo_evento=tipo_evento.upper().strip(),
            descricao=descricao.strip(),
            nivel=nivel_upper
        )

        self.historico_logs.append(novo_log)
        self.proximo_id += 1

        try:
            logs_db.registar(modulo, novo_log.tipo_evento, novo_log.descricao, nivel_upper)
        except Exception as erro:
            print("Erro ao gravar log na base de dados:", erro)

        logger_dedicado = self._obter_logger_modulo(modulo)
        msg_formatada = f"-> {novo_log.tipo_evento}: {novo_log.descricao}"

        if nivel_upper == "WARNING":
            logger_dedicado.warning(msg_formatada)
        elif nivel_upper == "CRITICAL":
            logger_dedicado.critical(msg_formatada)
        else:
            logger_dedicado.info(msg_formatada)
        return True

    def apagar_por_id(self, id_log: int) -> bool:
        for log in self.historico_logs:
            if log.id_log == id_log:
                self.historico_logs.remove(log)
                logs_db.apagar_por_id(id_log)
                return True
        return False

    def carregar_do_bd(self, limite: int = 500):
        """Carrega da base de dados o histórico das sessões anteriores."""
        for linha in logs_db.listar(limite):
            self.historico_logs.append(RegistoLog(
                id_log=linha["id"],
                data_hora=datetime.strptime(linha["data_hora"], "%Y-%m-%d %H:%M:%S"),
                modulo=linha["modulo"],
                tipo_evento=linha["tipo_evento"],
                descricao=linha["descricao"],
                nivel=linha["nivel"]
            ))

            self.proximo_id = max(self.proximo_id, linha["id"] + 1)

        return len(self.historico_logs)

    def listar_todos(self):
        return self.historico_logs

    def filtrar_por_modulo(self, modulo: str):
        return [log for log in self.historico_logs if log.modulo == modulo.upper().strip()]

    def ler_ficheiro_log_modulo(self, modulo: str):
        nome_ficheiro = modulo.lower().strip().replace(" ", "_")
        caminho_ficheiro = PASTA_LOGS / f"modulo_{nome_ficheiro}.log"
        if not caminho_ficheiro.exists():
            return [f"Nenhum registo físico encontrado para o módulo {modulo.upper()}."]
        with open(str(caminho_ficheiro), "r", encoding="utf-8") as f:
            return f.readlines()


class InterfaceGraficaLogs:
    def __init__(self, gestor: GestorLogs, master_frame: tk.Frame = None):
        self.gestor = gestor

        # Se receber um master_frame, acopla-se a ele. Caso contrário, gera uma janela própria.
        if master_frame:
            self.root = master_frame
            self.is_subframe = True
        else:
            self.root = tk.Tk()
            self.root.title("Sistema de Gestão de Logs")
            self.root.geometry("950x650")
            self.root.minsize(850, 550)
            self.style = ttk.Style()
            self.style.theme_use("clam")
            self.is_subframe = False

        self._construir_interface()
        self.atualizar_tabela_memoria()

    def _construir_interface(self):
        # Container principal para isolamento da interface
        self.main_container = ttk.Frame(self.root, padding=10)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        painel_esquerdo = ttk.LabelFrame(self.main_container, text=" Operações ", padding=15)
        painel_esquerdo.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # Formulário
        ttk.Label(painel_esquerdo, text="Módulo:").pack(anchor=tk.W, pady=(5, 2))
        self.cb_modulo = ttk.Combobox(painel_esquerdo, values=MODULOS_PERMITIDOS, state="readonly", width=25)
        self.cb_modulo.pack(fill=tk.X, pady=(0, 10))
        self.cb_modulo.set(MODULOS_PERMITIDOS[0])

        ttk.Label(painel_esquerdo, text="Nível:").pack(anchor=tk.W, pady=(5, 2))
        self.cb_nivel = ttk.Combobox(painel_esquerdo, values=NIVEIS_PERMITIDOS, state="readonly", width=25)
        self.cb_nivel.pack(fill=tk.X, pady=(0, 10))
        self.cb_nivel.set(NIVEIS_PERMITIDOS[0])

        ttk.Label(painel_esquerdo, text="Tipo de Evento:").pack(anchor=tk.W, pady=(5, 2))
        self.txt_tipo = ttk.Entry(painel_esquerdo, width=28)
        self.txt_tipo.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(painel_esquerdo, text="Descrição:").pack(anchor=tk.W, pady=(5, 2))
        self.txt_desc = ttk.Entry(painel_esquerdo, width=28)
        self.txt_desc.pack(fill=tk.X, pady=(0, 15))

        btn_gravar = ttk.Button(painel_esquerdo, text="Gravar Log Manual", command=self.submeter_log)
        btn_gravar.pack(fill=tk.X, ipady=3, pady=(0, 5))

        btn_apagar = ttk.Button(painel_esquerdo, text="Apagar Selecionado", command=self.apagar_log_selecionado)
        btn_apagar.pack(fill=tk.X, ipady=3, pady=(0, 25))

        lbl_importar = ttk.Label(painel_esquerdo, text="Central de Importação:", font=("Helvetica", 9, "bold"))
        lbl_importar.pack(anchor=tk.W, pady=(5, 5))

        btn_importar_hub = ttk.Button(
            painel_esquerdo,
            text="Importar Logs (Ficheiro/Pasta)...",
            command=self.abrir_hub_importacao
        )
        btn_importar_hub.pack(fill=tk.X, ipady=5)

        painel_direito = ttk.Frame(self.main_container, padding=10)
        painel_direito.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        zona_filtros = ttk.Frame(painel_direito)
        zona_filtros.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(zona_filtros, text="Filtrar Módulo:").pack(side=tk.LEFT, padx=(0, 5))
        self.cb_filtro = ttk.Combobox(zona_filtros, values=["(TODOS)"] + MODULOS_PERMITIDOS, state="readonly", width=15)
        self.cb_filtro.pack(side=tk.LEFT, padx=5)
        self.cb_filtro.set("(TODOS)")
        self.cb_filtro.bind("<<ComboboxSelected>>", lambda e: self.atualizar_tabela_memoria())

        btn_ver_ficheiro = ttk.Button(zona_filtros, text="Ver Ficheiro Físico (.log)", command=self.janela_ficheiro_fisico)
        btn_ver_ficheiro.pack(side=tk.RIGHT, padx=5)

        aba_tabela = ttk.Frame(painel_direito)
        aba_tabela.pack(fill=tk.BOTH, expand=True)

        colunas = ("id", "data", "nivel", "modulo", "evento", "descricao")
        self.tabela = ttk.Treeview(aba_tabela, columns=colunas, show="headings")

        self.tabela.heading("id", text="ID")
        self.tabela.heading("data", text="Data/Hora")
        self.tabela.heading("nivel", text="Nível")
        self.tabela.heading("modulo", text="Módulo")
        self.tabela.heading("evento", text="Evento")
        self.tabela.heading("descricao", text="Descrição")

        self.tabela.column("id", width=40, anchor=tk.CENTER)
        self.tabela.column("data", width=130, anchor=tk.CENTER)
        self.tabela.column("nivel", width=80, anchor=tk.CENTER)
        self.tabela.column("modulo", width=120, anchor=tk.CENTER)
        self.tabela.column("evento", width=100, anchor=tk.W)
        self.tabela.column("descricao", width=250, anchor=tk.W)

        scroll_y = ttk.Scrollbar(aba_tabela, orient=tk.VERTICAL, command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scroll_y.set)
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

    def abrir_hub_importacao(self):
        janela_hub = tk.Toplevel(self.root.winfo_toplevel())
        janela_hub.title("Modo de Importação")
        janela_hub.geometry("380x150")
        janela_hub.resizable(False, False)
        janela_hub.transient(self.root.winfo_toplevel())
        janela_hub.grab_set()

        lbl = ttk.Label(janela_hub, text="O que deseja importar para o sistema?", font=("Helvetica", 10, "bold"))
        lbl.pack(pady=15)

        zona_botoes = ttk.Frame(janela_hub)
        zona_botoes.pack(fill=tk.X, padx=20, pady=10)

        def acao_ficheiros():
            janela_hub.destroy()
            self.executar_importacao_ficheiros()

        def acao_pasta():
            janela_hub.destroy()
            self.executar_importacao_pasta()

        btn_f = ttk.Button(zona_botoes, text="Ficheiro(s) .log", command=acao_ficheiros)
        btn_f.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5, ipady=4)

        btn_p = ttk.Button(zona_botoes, text="Pasta Completa", command=acao_pasta)
        btn_p.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=5, ipady=4)

    def executar_importacao_ficheiros(self):
        ficheiros = filedialog.askopenfilenames(
            title="Selecionar Ficheiros de Log",
            filetypes=[("Ficheiros de Log", "*.log"), ("Todos os Ficheiros", "*.*")]
        )
        if not ficheiros:
            return

        total_linhas = 0
        for f in ficheiros:
            total_linhas += self.gestor.carregar_de_ficheiro(Path(f))

        self.atualizar_tabela_memoria()
        messagebox.showinfo("Sucesso", f"Importação concluída!\nForam carregados {total_linhas} registos com sucesso.")

    def executar_importacao_pasta(self):
        pasta = filedialog.askdirectory(title="Selecionar Pasta com Ficheiros .log")
        if not pasta:
            return

        caminho_pasta = Path(pasta)
        ficheiros_log = list(caminho_pasta.glob("*.log"))

        if not ficheiros_log:
            messagebox.showwarning("Aviso", "Nenhum ficheiro com a extensão '.log' foi encontrado na pasta selecionada.")
            return

        total_linhas = 0
        for f in ficheiros_log:
            total_linhas += self.gestor.carregar_de_ficheiro(f)

        self.atualizar_tabela_memoria()
        messagebox.showinfo("Sucesso", f"Pasta processada!\nForam importados {total_linhas} registos a partir de {len(ficheiros_log)} ficheiros.")

    def submeter_log(self):
        mod = self.cb_modulo.get()
        niv = self.cb_nivel.get()
        tipo = self.txt_tipo.get().strip()
        desc = self.txt_desc.get().strip()

        if not tipo or not desc:
            messagebox.showwarning("Aviso", "Por favor preencha todos os campos textuais.")
            return

        sucesso = self.gestor.registar(mod, tipo, desc, niv)
        if sucesso:
            messagebox.showinfo("Sucesso", "Log gravado no ficheiro físico e em memória!")
            self.txt_tipo.delete(0, tk.END)
            self.txt_desc.delete(0, tk.END)
            self.atualizar_tabela_memoria()
        else:
            messagebox.showerror("Erro", "Falha na validação dos dados.")

    def apagar_log_selecionado(self):
        item_selecionado = self.tabela.selection()
        if not item_selecionado:
            messagebox.showwarning("Aviso", "Por favor, selecione primeiro um log na tabela para o apagar.")
            return

        valores = self.tabela.item(item_selecionado, "values")
        id_log = int(valores[0])

        if messagebox.askyesno("Confirmar", f"Tem a certeza que deseja apagar o log com ID {id_log} da memória?"):
            if self.gestor.apagar_por_id(id_log):
                messagebox.showinfo("Sucesso", f"O log com o ID {id_log} foi removido.")
                self.atualizar_tabela_memoria()

    def atualizar_tabela_memoria(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        filtro = self.cb_filtro.get()
        logs = self.gestor.listar_todos() if filtro == "(TODOS)" else self.gestor.filtrar_por_modulo(filtro)

        for l in logs:
            self.tabela.insert("", tk.END, values=(
                l.id_log,
                l.data_hora.strftime("%d/%m/%Y %H:%M:%S"),
                l.nivel,
                l.modulo,
                l.tipo_evento,
                l.descricao
            ))

    def janela_ficheiro_fisico(self):
        modulo_selecionado = self.cb_filtro.get()
        if modulo_selecionado == "(TODOS)":
            messagebox.showinfo("Informação", "Escolha um módulo específico no filtro ao lado para ler o ficheiro físico.")
            return

        linhas = self.gestor.ler_ficheiro_log_modulo(modulo_selecionado)
        janela_txt = tk.Toplevel(self.root.winfo_toplevel())
        janela_txt.title(f"Ficheiro Físico - {modulo_selecionado}")
        janela_txt.geometry("600x400")

        txt_area = tk.Text(janela_txt, wrap=tk.WORD, padx=10, pady=10)
        scroll = ttk.Scrollbar(janela_txt, command=txt_area.yview)
        txt_area.configure(yscrollcommand=scroll.set)

        txt_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        for lambda_linha in linhas:
            txt_area.insert(tk.END, lambda_linha)
        txt_area.configure(state="disabled")

    def iniciar(self):
        if not self.is_subframe:
            self.root.mainloop()

_gestor_global = None

def inicializar():
    global _gestor_global
    if _gestor_global is None:
        _gestor_global = GestorLogs()
        _gestor_global.carregar_do_bd()
        _gestor_global.registar("LOGS", "INICIALIZACAO", "Módulo de logs múltiplos inicializado.")
    return _gestor_global

def menu(container=None):
    if _gestor_global is None:
        inicializar()
    interface = InterfaceGraficaLogs(_gestor_global, master_frame=container)
    interface.iniciar()

def ejecutar():
    inicializar()
    menu()

if __name__ == "__main__":
    ejecutar()