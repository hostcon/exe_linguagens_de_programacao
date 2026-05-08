import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("StringVar Demo")

# Criar a variável (sempre ligada a uma janela raiz)
nome_var = tk.StringVar(value="Python")

# Entry VINCULADO: digitar muda nome_var
entry = ttk.Entry(root, textvariable=nome_var, width=25)
entry.pack(padx=20, pady=10)

# Label VINCULADO: atualiza automaticamente quando nome_var muda
preview = ttk.Label(root, textvariable=nome_var, font=("Arial", 14, "bold"))
preview.pack(pady=6)

# Ler o valor via código
def mostrar():
    print("Valor atual:", nome_var.get())

# Definir valor via código (atualiza todos os widgets vinculados)
def resetar():
    nome_var.set("")  # limpa entry E label automaticamente

ttk.Button(root, text="Mostrar", command=mostrar).pack(pady=4)
ttk.Button(root, text="Limpar", command=resetar).pack(pady=4)

root.mainloop()