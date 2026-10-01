"""
Ponto de entrada do Integrated Security System.

Camadas:
    1. interface_grafica -> interfaces tkinter
    2. modulos            -> logica de negocio
    3. base_dados         -> persistencia (SQLite)
"""

from interface_grafica import login


if __name__ == "__main__":
    login.abrir()
