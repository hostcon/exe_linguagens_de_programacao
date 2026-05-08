import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Layout com Frames")
root.geometry("500x300")

# Frame superior - cabeçalho
frm_topo = ttk.Frame(root, padding=10)
frm_topo.pack(fill=tk.X)

ttk.Label(frm_topo, text="Sistema de Cadastro",
          font=("Arial", 16, "bold")).pack()

# Frame central - conteúdo principal (expandível)
frm_central = ttk.Frame(root, padding=10)
frm_central.pack(fill=tk.BOTH, expand=True)

ttk.Label(frm_central, text="[Área de conteúdo]").pack(expand=True)

# Frame inferior - rodapé com botões
frm_rodape = ttk.Frame(root, padding=6)
frm_rodape.pack(fill=tk.X, side=tk.BOTTOM)

ttk.Button(frm_rodape, text="Cancelar").pack(side=tk.RIGHT, padx=4)
ttk.Button(frm_rodape, text="Salvar").pack(side=tk.RIGHT, padx=4)
ttk.Label(frm_rodape, text="Pronto.").pack(side=tk.LEFT)

root.mainloop()