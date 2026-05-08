import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Cores de Fundo")
root.geometry("480x320")

# Cor de fundo da janela principal
root.configure(background="#1E3A5F")  # azul escuro

# Frame clássico com cor
frm_topo = tk.Frame(root, bg="#2E6DA4", padx=12, pady=10)
frm_topo.pack(fill=tk.X)

lbl_topo = tk.Label(frm_topo,
                    text="Cabeçalho Colorido",
                    font=("Arial", 14, "bold"),
                    bg="#2E6DA4",
                    fg="white")
lbl_topo.pack()

# Frame central branco
frm_central = tk.Frame(root, bg="white", padx=20, pady=20)
frm_central.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

tk.Label(frm_central,
         text="Área de conteúdo (fundo branco)",
         bg="white", fg="#333333").pack()

# Trocar cor da janela por botão
cores = ["#1E3A5F", "#1A6B3C", "#6B1A1A", "#3D1A6B"]
idx = [0]

def alternar_cor():
    idx[0] = (idx[0] + 1) % len(cores)
    root.configure(bg=cores[idx[0]])
    frm_topo.configure(bg=cores[idx[0]])
    lbl_topo.configure(bg=cores[idx[0]])

tk.Button(frm_central, text="Alternar cor de fundo",
          command=alternar_cor,
          bg="#FFC107", fg="#333333").pack(pady=10)

root.mainloop()