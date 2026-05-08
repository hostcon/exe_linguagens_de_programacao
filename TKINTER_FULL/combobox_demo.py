import tkinter as tk
from tkinter import ttk

root = tk.Tk()

estado_var = tk.StringVar()
estados = ["AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"]

ttk.Label(root, text="Estado:").pack(padx=20, pady=(16,4))
combo = ttk.Combobox(root, textvariable=estado_var, values=estados, state="readonly", width=8)
combo.set("Selecione")
combo.pack(padx=20, pady=4)

# Evento disparado quando o usuário seleciona
combo.bind("<<ComboboxSelected>>", lambda e: print("Selecionado:", estado_var.get()))

root.mainloop()