import tkinter as tk

root = tk.Tk()
root.title("Relógio")

label = tk.Label(root, font=("Arial", 32))
label.pack(padx=30, pady=20)

def atualizar():
    from datetime import datetime
    agora = datetime.now().strftime("%H:%M:%S")
    label.config(text=agora)
    root.after(1000, atualizar)  # reagenda após 1000ms

atualizar()  # chama a primeira vez
root.mainloop()