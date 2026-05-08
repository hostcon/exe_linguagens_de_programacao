import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("App com Toolbar")
root.geometry("650x400")

# — Toolbar —
toolbar = tk.Frame(root, bg="#EEEEEE", relief=tk.GROOVE, bd=1)
toolbar.pack(side=tk.TOP, fill=tk.X)


# Função auxiliar: cria botão na toolbar com hover e tooltip
def btn_toolbar(pai, emoji, texto_tooltip, acao):
    btn = tk.Button(pai, text=emoji, bg="#EEEEEE", fg="#333333",
                    activebackground="#CCCCCC",
                    font=("Arial", 14),
                    relief=tk.FLAT,
                    width=2, padx=4, pady=4,
                    cursor="hand2",
                    command=acao)
    btn.pack(side=tk.LEFT, padx=2, pady=2)

    # Tooltip simples
    tip = tk.Label(root, text=texto_tooltip,
                   bg="#FFFFFF", relief=tk.SOLID, bd=1,
                   font=("Arial", 9))

    def mostrar(e):
        tip.place(x=btn.winfo_x(), y=toolbar.winfo_height() + 4)

    def esconder(e):
        tip.place_forget()

    btn.bind("<Enter>", mostrar)
    btn.bind("<Leave>", esconder)
    btn.bind("<Enter>", lambda e: btn.configure(bg="#CCCCCC"), add="+")
    btn.bind("<Leave>", lambda e: btn.configure(bg="#EEEEEE"), add="+")
    return btn


# Separador na toolbar
def sep_toolbar(pai):
    tk.Frame(pai, width=1, bg="#BBBBBB").pack(side=tk.LEFT, fill=tk.Y, padx=4, pady=4)


# Adicionar botões
btn_toolbar(toolbar, "📄", "Novo arquivo", lambda: print("Novo"))
btn_toolbar(toolbar, "📂", "Abrir arquivo", lambda: print("Abrir"))
btn_toolbar(toolbar, "💾", "Salvar arquivo", lambda: print("Salvar"))
sep_toolbar(toolbar)
btn_toolbar(toolbar, "✂️", "Recortar", lambda: print("Recortar"))
btn_toolbar(toolbar, "📋", "Copiar", lambda: print("Copiar"))
btn_toolbar(toolbar, "📌", "Colar", lambda: print("Colar"))
sep_toolbar(toolbar)
btn_toolbar(toolbar, "↩️", "Desfazer", lambda: print("Desfazer"))
btn_toolbar(toolbar, "↪️", "Refazer", lambda: print("Refazer"))

# — Área de trabalho
txt = tk.Text(root, font=("Courier New", 12), wrap=tk.WORD, undo=True)
txt.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

root.mainloop()