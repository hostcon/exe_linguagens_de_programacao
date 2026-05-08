import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Formulário com Grid")

campos = ["Nome", "E-mail", "Telefone", "Cargo"]
entries = {}

for i, campo in enumerate(campos):
    ttk.Label(root, text=campo + ":").grid(
        row=i, column=0,
        sticky="w",  # alinha à esquerda
        padx=12, pady=6)
    e = ttk.Entry(root, width=30)
    e.grid(row=i, column=1, padx=12, pady=6, sticky="ew")
    entries[campo] = e

# Combobox ocupa 2 colunas (columnspan)
ttk.Label(root, text="Nível:").grid(row=4, column=0, padx=12, pady=6, sticky="w")
nivel = ttk.Combobox(root, values=["Júnior", "Pleno", "Sênior"], state="readonly")
nivel.grid(row=4, column=1, padx=12, pady=6, sticky="ew")

# Botão ocupa 2 colunas
ttk.Button(root, text="Salvar").grid(row=5, column=0, columnspan=2, pady=12)

# Coluna 1 expande com a janela
root.columnconfigure(1, weight=1)

root.mainloop()