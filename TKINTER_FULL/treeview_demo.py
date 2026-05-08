import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Tabela de Usuários")
root.geometry("600x380")

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Definir colunas
colunas = ("id", "nome", "email", "nivel")

tree = ttk.Treeview(frame, columns=colunas, show="headings", height=12)

# Configurar cabeçalhos e larguras
config = {
    "id": (50, "ID", "center"),
    "nome": (160, "Nome", "w"),
    "email": (200, "E-mail", "w"),
    "nivel": (100, "Nivel", "center"),
}

for col, (w, label, anchor) in config.items():
    tree.heading(col, text=label)
    tree.column(col, width=w, anchor=anchor)

# Inserir dados
dados = [
    (1, "Ana Lima", "ana@email.com", "Sênior"),
    (2, "Bruno Melo", "bruno@email.com", "Pleno"),
    (3, "Carla Rocha", "carla@email.com", "Júnior"),
]

for i, row in enumerate(dados):
    tag = "par" if i % 2 == 0 else "impar"
    tree.insert("", tk.END, values=row, tags=(tag,))

tree.tag_configure("par", background="#F4F6F9")
tree.tag_configure("impar", background="#FFFFFF")

# Scrollbar
scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scroll.set)
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Evento de seleção
def ao_selecionar(event):
    sel = tree.selection()
    if sel:
        vals = tree.item(sel[0], "values")
        print(f"Selecionado: {vals[1]} ({vals[2]})")

tree.bind("<<TreeviewSelect>>", ao_selecionar)

root.mainloop()