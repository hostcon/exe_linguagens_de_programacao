import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")

# side: TOP (padrão), BOTTOM, LEFT, RIGHT
ttk.Label(root, text="Topo", background="#4A90C4", foreground="white").pack(side=tk.TOP, fill=tk.X)
ttk.Label(root, text="Rodapé", background="#1E3A5F", foreground="white").pack(side=tk.BOTTOM, fill=tk.X)
ttk.Label(root, text="Esq", background="#28A745", foreground="white").pack(side=tk.LEFT, fill=tk.Y)
ttk.Label(root, text="Dir", background="#FFC107").pack(side=tk.RIGHT, fill=tk.Y)

# expand=True: ocupa todo o espaço restante
ttk.Label(root, text="Centro", background="#F4F6F9").pack(expand=True, fill=tk.BOTH)

# padx, pady: espaço externo; ipadx, ipady: interno
ttk.Button(root, text="OK").pack(pady=10, padx=20)

root.mainloop()