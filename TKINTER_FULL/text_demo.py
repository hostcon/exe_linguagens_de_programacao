import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Editor Simples")

# Frame com Text + Scrollbar
frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

texto = tk.Text(frame, wrap=tk.WORD, font=("Arial", 11), undo=True)
scroll = ttk.Scrollbar(frame, command=texto.yview)
texto.configure(yscrollcommand=scroll.set)

texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Inserir texto inicial
texto.insert("1.0", "Digite aqui seu texto...\n")

# Ler conteúdo completo
# conteudo = texto.get("1.0", tk.END)

# Limpar tudo
# texto.delete("1.0", tk.END)

# Tag para destacar texto
texto.tag_configure("destaque", foreground="blue", font=("Arial", 11, "bold"))
# texto.tag_add("destaque", "1.0", "1.7")

root.mainloop()