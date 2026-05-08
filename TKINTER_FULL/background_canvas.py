import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Background com Imagem")
root.geometry("600x400")

# Canvas ocupa toda a janela
canvas = tk.Canvas(root, width=600, height=400)
canvas.pack(fill=tk.BOTH, expand=True)

# Carrega e posiciona a imagem de fundo
try:
    bg_img = tk.PhotoImage(file="background.png")
    canvas.create_image(0, 0, anchor="nw", image=bg_img)
    canvas.image = bg_img  # mantém referência
except:
    canvas.create_rectangle(0, 0, 600, 400, fill="#1E3A5F")
    canvas.create_text(300, 200, text="Background não encontrado",
                       fill="white", font=("Arial", 16))

# Adicionar widgets SOBRE o canvas
frm_login = tk.Frame(canvas, bg="white", relief=tk.RAISED, bd=2, padx=30, pady=30)

tk.Label(frm_login, text="Login", bg="white", font=("Arial", 18, "bold"),
         fg="#1E3A5F").pack(pady=(0, 16))

tk.Label(frm_login, text="Usuário:", bg="white").pack(anchor="w")
entry_usr = tk.Entry(frm_login, width=25, font=("Arial", 11))
entry_usr.pack(pady=(2, 10))

tk.Label(frm_login, text="Senha:", bg="white").pack(anchor="w")
entry_pwd = tk.Entry(frm_login, width=25, show="*", font=("Arial", 11))
entry_pwd.pack(pady=(2, 16))

tk.Button(frm_login, text="Entrar",
          bg="#2E6DA4", fg="white",
          font=("Arial", 11, "bold"),
          relief=tk.FLAT, padx=20, pady=8).pack(fill=tk.X)

# Posiciona o frame no centro do canvas
canvas.create_window(300, 200, anchor="center", window=frm_login)

root.mainloop()