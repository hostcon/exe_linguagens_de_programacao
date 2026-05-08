import tkinter as tk
from tkinter import ttk

root = tk.Tk()

ttk.Label(root, text="Quantidade:").pack(padx=20, pady=(16,4))
spin = ttk.Spinbox(root,
                   from_=1, to=100, increment=1,
                   width=10, justify="center")
spin.set(1)
spin.pack(padx=20, pady=4)

ttk.Button(root, text="Ver valor",
           command=lambda: print("Valor:", spin.get())).pack(pady=8)

root.mainloop()