import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Estilos Personalizados")
root.geometry("400x300")

style = ttk.Style()
style.theme_use("clam")

# Estilo para botão primário (azul)
style.configure("Primario.TButton",
                font=("Arial", 11, "bold"),
                foreground="white",
                background="#2E6DA4",
                padding=10,
                relief="flat")
style.map("Primario.TButton",
          background=[("active", "#1E3A5F"), ("pressed", "#1E3A5F")])

# Estilo para botão de perigo (vermelho)
style.configure("Perigo.TButton",
                font=("Arial", 11),
                foreground="white",
                background="#DC3545",
                padding=10)

# Estilo para Label de título
style.configure("Titulo.TLabel",
                font=("Arial", 18, "bold"),
                foreground="#1E3A5F")

# Usar os estilos
ttk.Label(root, text="Bem-vindo!", style="Titulo.TLabel").pack(pady=20)
ttk.Button(root, text="Salvar", style="Primario.TButton").pack(pady=6)
ttk.Button(root, text="Excluir", style="Perigo.TButton").pack(pady=6)

root.mainloop()