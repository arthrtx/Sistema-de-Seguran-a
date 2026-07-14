import os

# Coloque o caminho onde quer criar a pasta
caminho = "C:\Temp"

pasta = os.path.join(caminho, "MinhaPasta")
os.makedirs(pasta, exist_ok=True)

faces = os.path.join(pasta, "faces")
os.makedirs(faces, exist_ok=True)

arquivo = os.path.join(pasta, "arquivo.txt")
with open(arquivo, "w") as f:
    pass

print("Criado com sucesso!")