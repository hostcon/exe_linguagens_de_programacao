import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.geometry("400x300")

# Absoluto (pixel)
ttk.Label(root, text="x=20, y=20", background="lightblue").place(x=20, y=20)

# Relativo ao tamanho da janela
ttk.Label(root, text="Centro (50%,50%)", background="lightyellow").place(relx=0.5, rely=0.5, anchor="center")

# Canto inferior direito
ttk.Button(root, text="Sair", command=root.destroy).place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

root.mainloop()