import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# 1. Janela raiz
root.title("Meu App")
root.geometry("400x200")  # largura x altura em pixels

label = ttk.Label(root, text="Olá!")  # 2. Widget
label.pack(pady=20)

root.mainloop()  # 3. Loop de eventos