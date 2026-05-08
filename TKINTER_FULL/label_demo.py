import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Label Demo")

# Label simples
lbl1 = ttk.Label(root, text="Texto simples")
lbl1.pack(pady=6)

# Label com fonte e cor
lbl2 = ttk.Label(root, text="Destaque", font=("Arial", 16, "bold"), foreground="navy")
lbl2.pack(pady=6)

# Atualizar texto dinamicamente
lbl3 = ttk.Label(root, text="Aguardando...")
lbl3.pack(pady=6)
root.after(2000, lambda: lbl3.config(text="Atualizado!"))

# Label com imagem (arquivo PNG)
# img = tk.PhotoImage(file="logo.png")
# lbl_img = ttk.Label(root, image=img)
# lbl_img.image = img  # manter referência!
# lbl_img.pack()

root.mainloop()