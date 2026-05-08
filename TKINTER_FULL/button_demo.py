import tkinter as tk
from tkinter import ttk

root = tk.Tk()
contador = [0]  # lista para permitir mutação em closure

def incrementar():
    contador[0] += 1
    lbl.config(text=f"Cliques: {contador[0]}")

lbl = ttk.Label(root, text="Cliques: 0", font=("Arial", 14))
lbl.pack(pady=12)

# Botão com command direto
btn1 = ttk.Button(root, text="Incrementar", command=incrementar)
btn1.pack(pady=4)

# Botão com lambda (para passar argumento)
btn2 = ttk.Button(root, text="Resetar", command=lambda: (contador.__setitem__(0, 0), lbl.config(text="Cliques: 0")))
btn2.pack(pady=4)

# Botão desabilitado
btn3 = ttk.Button(root, text="Inativo", state="disabled")
btn3.pack(pady=4)

root.mainloop()