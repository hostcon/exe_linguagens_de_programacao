import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Listbox Demo")

frame = ttk.Frame(root)
frame.pack(padx=12, pady=12)

lista = tk.Listbox(frame, selectmode=tk.EXTENDED, width=30, height=8)
scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=lista.yview)
lista.configure(yscrollcommand=scroll.set)
lista.pack(side=tk.LEFT, fill=tk.BOTH)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

cidades = ["São Paulo", "Rio de Janeiro", "Curitiba", "Porto Alegre",
           "Belo Horizonte", "Florianópolis", "Salvador", "Recife"]
for c in cidades:
    lista.insert(tk.END, c)

def mostrar_selecionados():
    indices = lista.curselection()
    selecionados = [lista.get(i) for i in indices]
    print("Selecionados:", selecionados)

ttk.Button(root, text="Ver seleção", command=mostrar_selecionados).pack(pady=8)

root.mainloop()