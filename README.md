# Sistema Integrado de Segurança

App de desktop em Python para gerir utilizadores, permissões e registos de acesso de um
sistema de segurança. Interface em Tkinter, dados em SQLite.

Este é um **trabalho de grupo** (formação IEFP). Cada elemento ficou responsável por um
módulo e a parte de interface foi revista e arrumada por todos no fim, para ficar coerente
entre os módulos.

## Estado atual

Feito e a funcionar:

- login e logout com bloqueio temporário ao fim de 3 tentativas
- registo de contas (utilizador ou administrador)
- lista de utilizadores com criar, editar e eliminar
- módulo de controlo de acessos: permissões, histórico de logins e estatísticas
- módulo de logs com registo por módulo, filtro, importação de ficheiros `.log` e
  histórico guardado em base de dados
- persistência em SQLite (utilizadores, acessos e logs)

**Ainda não está feito** — os separadores existem no menu lateral mas abrem apenas um
ecrã vazio, os módulos estão por desenvolver:

- Câmaras (live view, gravação de vídeo, deteção de movimento)
- Sensores e alarmes
- Relatórios
- Backups
- Dashboard com os dados reais do sistema (por agora mostra só "SISTEMA ONLINE")
- As passwords estão guardadas em texto simples na base de dados, o que tem de ser
  corrigido antes de isto ser usado a sério

## Como correr

Windows, com Python 3.11 ou superior instalado:

```bat
run.bat
```

Ou diretamente:

```bash
python main.py
```

Dependências: `tkinter` (vem com o Python) e `opencv-python`, para o Face ID e para o
módulo de câmaras:

```bash
pip install opencv-python
```

### Conta de administração

Existe uma conta de administração temporária para quem testar:

| username | password |
| -------- | -------- |
| adm      | adm      |

Depois de entrar, vai a **Utilizadores** e cria a conta definitiva, e elimina esta.

## Onde ficam os dados

Nada é escrito dentro da pasta do projeto. Tudo vai para
`%LOCALAPPDATA%\SecuritySystem`:

```
dados/security_system.db   base de dados SQLite
logs/                      um ficheiro .log por módulo
faces/                     fotografias do Face ID
utilizadores.json.migrado  cópia dos utilizadores anteriores à migração
logs.txt                   registo do sistema
```

Assim dá para apagar a pasta do projeto sem perder nada, e o `.exe` funciona a partir de
qualquer sítio.

## Estrutura

```
main.py              ponto de entrada
run.bat              atalho para arranque no Windows
login.spec           configuração do PyInstaller
interface_grafica/   login, painel principal e janelas de cada módulo
modulos/             autenticação, utilizadores, acessos, câmaras, registos, config
base_dados/          SQLite: esquema, utilizadores, acessos, logs e migração
```

O código está separado em três camadas: a interface não fala com a base de dados
diretamente, passa sempre pelos módulos.

## Gerar o executável

```bash
pip install pyinstaller
pyinstaller login.spec
```

Sai um `dist/SecuritySystem.exe` com tudo incluído (Python, Tkinter e OpenCV), que funciona
sem precisar de instalar nada. O `.exe` da versão atual está anexado na release v1.0.

## Notas

- O ficheiro `base_dados` em SQLite é criado automaticamente na primeira execução, com as
  tabelas e colunas em falta caso o esquema tenha mudado.
- Quem vier do código antigo (ficheiros `.py` na raiz e `sistema_seguranca.db`) tem a
  migração automática para a pasta nova e para a base de dados atual.
