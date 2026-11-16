import customtkinter as ctk
from tkinter import messagebox

# ==================================
# Configurações de Tema (Opcional)
# ==================================
ctk.set_appearance_mode("dark")  # Modos: "system", "light", "dark"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

# ==================================
# Janela Principal
# ==================================
janela = ctk.CTk()
janela.title("Sistema de Login")
janela.geometry("350x220") # Ajustei levemente a altura para o visual do CTk

# ==================================
# Função Login
# ==================================
def login():
    usuario = edt_login.get()
    senha = edt_senha.get()

    if usuario == "wagner" and senha == "123":
        # Usando CTkToplevel para manter o tema na nova janela
        nova_janela = ctk.CTkToplevel(janela) 
        nova_janela.title("Menu Principal")
        nova_janela.geometry("300x200")

        lbl_boas_vindas = ctk.CTkLabel(
            nova_janela,
            text=f"Bem-vindo, {usuario}!",
            font=("Arial", 14)
        )
        lbl_boas_vindas.pack(pady=30)
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos!")

# ==================================
# Widgets (Login, Senha, Botão)
# ==================================

# Label Login
lbl_login = ctk.CTkLabel(janela, text="Login:")
lbl_login.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Campo Login
edt_login = ctk.CTkEntry(janela, width=200)
edt_login.grid(row=0, column=1, padx=10, pady=10)

# Label Senha
lbl_senha = ctk.CTkLabel(janela, text="Senha:")
lbl_senha.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Campo Senha
# O parâmetro 'show="*"' funciona da mesma forma no CTkEntry
edt_senha = ctk.CTkEntry(janela, width=200, show="*")
edt_senha.grid(row=1, column=1, padx=10, pady=10)

# Botão Login
btn_login = ctk.CTkButton(
    janela,
    text="Entrar",
    command=login,
    width=100
)
btn_login.grid(row=2, column=0, columnspan=2, pady=20)

# ==================================
# Loop Principal
# ==================================
janela.mainloop()
