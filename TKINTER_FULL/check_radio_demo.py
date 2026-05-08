import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Check e Radio")

# — Checkbutton
ttk.Label(root, text="Habilidades:", font=("Arial", 11, "bold")).pack(anchor="w", padx=12, pady=(12,4))
habilidades = {"Python": tk.BooleanVar(), "Java": tk.BooleanVar(), "SQL": tk.BooleanVar()}
for nome, var in habilidades.items():
    ttk.Checkbutton(root, text=nome, variable=var).pack(anchor="w", padx=30)

# — Radiobutton
ttk.Label(root, text="Nivel:", font=("Arial", 11, "bold")).pack(anchor="w", padx=12, pady=(12,4))
nivel_var = tk.StringVar(value="junior")
niveis = [("Júnior", "junior"), ("Pleno", "pleno"), ("Sênior", "senior")]
for texto, val in niveis:
    ttk.Radiobutton(root, text=texto, variable=nivel_var, value=val).pack(anchor="w", padx=30)

def mostrar():
    selecionados = [n for n, v in habilidades.items() if v.get()]
    print(f"Habilidades: {selecionados} | Nivel: {nivel_var.get()}")

ttk.Button(root, text="Ver seleção", command=mostrar).pack(pady=12)

root.mainloop()