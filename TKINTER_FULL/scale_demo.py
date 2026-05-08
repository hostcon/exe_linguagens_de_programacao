import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Scale Demo")

valor_var = tk.IntVar(value=50)

ttk.Label(root, text="Volume:").pack(pady=(16, 4))
scale = tk.Scale(root,
                 variable=valor_var,
                 from_=0, to=100,
                 orient=tk.HORIZONTAL,
                 length=300,
                 tickinterval=25,
                 command=lambda v: lbl_val.config(text=f"Valor: {v}"))
scale.pack(padx=20)

lbl_val = ttk.Label(root, text="Valor: 50")
lbl_val.pack(pady=8)

root.mainloop()