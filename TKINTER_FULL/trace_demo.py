import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Busca em Tempo Real")

frutas = ["Abacaxi", "Banana", "Caju", "Goiaba", "Laranja", "Maçã", "Manga", "Maracujá", "Melancia", "Uva"]

busca_var = tk.StringVar()

ttk.Entry(root, textvariable=busca_var, width=30).pack(padx=12, pady=10)

listbox = tk.Listbox(root, height=8, width=30)
listbox.pack(padx=12, pady=4)

def filtrar(*args):  # *args ignora os parâmetros do trace
    termo = busca_var.get().lower()
    listbox.delete(0, tk.END)
    for f in frutas:
        if termo in f.lower():
            listbox.insert(tk.END, f)

# Chama filtrar() sempre que busca_var for modificada
busca_var.trace_add("write", filtrar)
filtrar()  # popula a lista inicialmente

root.mainloop()