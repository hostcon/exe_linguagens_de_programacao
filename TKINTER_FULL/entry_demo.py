import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Entry Demo")

# Entry simples
ttk.Label(root, text="Nome:").grid(row=0, column=0, padx=8, pady=6, sticky="w")
entry_name = ttk.Entry(root, width=25)
entry_name.grid(row=0, column=1, padx=8, pady=6)

# Entry com máscara de senha
ttk.Label(root, text="Senha:").grid(row=1, column=0, padx=8, pady=6, sticky="w")
entry_senha = ttk.Entry(root, width=25, show="*")
entry_senha.grid(row=1, column=1, padx=8, pady=6)

# Preenche automaticamente
entry_name.insert(0, "Usuário padrão")

resultado = ttk.Label(root, text="")
resultado.grid(row=3, column=0, columnspan=2, pady=8)

def ler_campos():
    nome = entry_name.get()
    senha = entry_senha.get()
    resultado.config(text=f"Nome: {nome} | Senha: {len(senha)} chars")

ttk.Button(root, text="Ler", command=ler_campos).grid(row=2, column=1, pady=4)

root.mainloop()