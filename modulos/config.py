from pathlib import Path

# Pasta onde os dados serão guardados
BASE_DIR = Path.home() / "AppData" / "Local" / "SecuritySystem"

# Migração da pasta antiga (nome em português)
_OLD_DIR = Path.home() / "AppData" / "Local" / "SistemaSeguranca"
if not BASE_DIR.exists() and _OLD_DIR.exists():
    _OLD_DIR.rename(BASE_DIR)

BASE_DIR.mkdir(parents=True, exist_ok=True)

ARQUIVO = BASE_DIR / "utilizadores.json"
ARQUIVO_LOG = BASE_DIR / "logs.txt"
ARQUIVO_ACESSOS = BASE_DIR / "acessos.json"
NOME_BD = "security_system.db"

PASTA_DADOS = BASE_DIR / "dados"
PASTA_LOGS = BASE_DIR / "logs"
PASTA_FACES = BASE_DIR / "faces"

for _pasta in (PASTA_DADOS, PASTA_LOGS, PASTA_FACES):
    _pasta.mkdir(parents=True, exist_ok=True)

BD = PASTA_DADOS / NOME_BD