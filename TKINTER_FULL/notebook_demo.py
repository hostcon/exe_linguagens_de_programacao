import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Interface com Abas")
root.geometry("500x350")

notebook = ttk.Notebook(root)
notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Aba 1 – Dados pessoais
aba1 = ttk.Frame(notebook, padding=12)
ttk.Label(aba1, text="Nome:").grid(row=0, column=0, sticky="w", pady=4)
ttk.Entry(aba1, width=25).grid(row=0, column=1, padx=8)
ttk.Label(aba1, text="E-mail:").grid(row=1, column=0, sticky="w", pady=4)
ttk.Entry(aba1, width=25).grid(row=1, column=1, padx=8)
notebook.add(aba1, text=" Pessoal ")

# Aba 2 – Configurações
aba2 = ttk.Frame(notebook, padding=12)
ttk.Checkbutton(aba2, text="Receber notificação(s)").pack(anchor="w")
ttk.Checkbutton(aba2, text="Modo escuro").pack(anchor="w")
notebook.add(aba2, text=" Config ")

# Aba 3 – Sobre
aba3 = ttk.Frame(notebook, padding=20)
ttk.Label(aba3, text="App v1.0", font=("Arial", 14, "bold")).pack()
ttk.Label(aba3, text="Desenvolvido com Python 3 + Tkinter").pack()
notebook.add(aba3, text=" i Sobre ")

# Detectar mudança de aba
notebook.bind("<<NotebookTabChanged>>", lambda e: print("Aba:", notebook.index("current")))

root.mainloop()