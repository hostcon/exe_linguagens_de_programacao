import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("LabelFrame Demo")

# LabelFrame para dados pessoais
grp_pessoa = ttk.LabelFrame(root, text="Dados Pessoais", padding=10)
grp_pessoa.pack(fill=tk.X, padx=12, pady=10)

ttk.Label(grp_pessoa, text="Nome:").grid(row=0, column=0, sticky="w", pady=4)
ttk.Entry(grp_pessoa, width=30).grid(row=0, column=1, padx=8)
ttk.Label(grp_pessoa, text="CPF:").grid(row=1, column=0, sticky="w", pady=4)
ttk.Entry(grp_pessoa, width=15).grid(row=1, column=1, padx=8, sticky="w")

# LabelFrame para endereço
grp_end = ttk.LabelFrame(root, text="Endereço", padding=10)
grp_end.pack(fill=tk.X, padx=12, pady=(0, 10))

ttk.Label(grp_end, text="Rua:").grid(row=0, column=0, sticky="w", pady=4)
ttk.Entry(grp_end, width=30).grid(row=0, column=1, padx=8)

root.mainloop()