import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Preferências")

# BooleanVar - True/False para cada checkbox
notif_email = tk.BooleanVar(value=True)
notif_sms = tk.BooleanVar(value=False)
modo_escuro = tk.BooleanVar(value=False)

ttk.Label(root, text="Notificações:", font=("Arial", 11, "bold")).pack(anchor="w", padx=14, pady=(14,4))
ttk.Checkbutton(root, text="E-mail", variable=notif_email).pack(anchor="w", padx=30)
ttk.Checkbutton(root, text="SMS", variable=notif_sms).pack(anchor="w", padx=30)

ttk.Label(root, text="Aparência:", font=("Arial", 11, "bold")).pack(anchor="w", padx=14, pady=(14,4))
ttk.Checkbutton(root, text="Modo escuro", variable=modo_escuro).pack(anchor="w", padx=30)

def salvar():
    config = {
        "email": notif_email.get(),
        "sms": notif_sms.get(),
        "dark": modo_escuro.get(),
    }
    print("Configurações:", config)

ttk.Button(root, text="Salvar", command=salvar).pack(pady=14)

root.mainloop()