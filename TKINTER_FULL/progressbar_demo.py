import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Progressbar")

# Modo determinado (valor 0-100)
progresso = ttk.Progressbar(root, length=300, mode="determinate", maximum=100)
progresso.pack(padx=20, pady=16)

valor = [0]

def avancar():
    if valor[0] < 100:
        valor[0] += 10
        progresso["value"] = valor[0]
        lbl.config(text=f"{valor[0]}%")

lbl = ttk.Label(root, text="0%")
lbl.pack()

ttk.Button(root, text="+10%", command=avancar).pack(pady=6)

# Modo indeterminado (carregando...)
spin_bar = ttk.Progressbar(root, length=300, mode="indeterminate")
spin_bar.pack(padx=20, pady=10)
spin_bar.start(12)  # inicia animação (ms entre cada passo)

root.mainloop()