import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("PanedWindow")
root.geometry("600x400")

painel = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
painel.pack(fill=tk.BOTH, expand=True)

# Painel esquerdo (lista)
frm_esq = ttk.Frame(painel, padding=8)
ttk.Label(frm_esq, text="Painel Esquerdo", font=("Arial", 11, "bold")).pack()
lista = tk.Listbox(frm_esq)
for i in range(10):
    lista.insert(tk.END, f"Item {i+1}")
lista.pack(fill=tk.BOTH, expand=True)
painel.add(frm_esq, weight=1)

# Painel direito (detalhes)
frm_dir = ttk.Frame(painel, padding=8)
ttk.Label(frm_dir, text="Painel Direito", font=("Arial", 11, "bold")).pack()
tk.Text(frm_dir, wrap=tk.WORD).pack(fill=tk.BOTH, expand=True)
painel.add(frm_dir, weight=2)

root.mainloop()