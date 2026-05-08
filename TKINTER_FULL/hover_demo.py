import tkinter as tk


def fazer_hover(widget, cor_normal, cor_hover, texto_normal=None, texto_hover=None):
    def on_enter(e):
        widget.configure(bg=cor_hover)
        if texto_hover and hasattr(widget, 'config'):
            if 'text' in widget.keys():
                widget.configure(text=texto_hover)

    def on_leave(e):
        widget.configure(bg=cor_normal)
        if texto_normal and hasattr(widget, 'config'):
            if 'text' in widget.keys():
                widget.configure(text=texto_normal)

    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)


root = tk.Tk()
root.title("Hover Demo - Completo")
root.geometry("500x450")
root.configure(bg="#F4F6F9")

# Título
tk.Label(root, text="Efeitos de Hover", font=("Arial", 18, "bold"),
         bg="#F4F6F9", fg="#1E3A5F").pack(pady=16)

# — Botão 1: Hover simples
btn1 = tk.Button(root, text="Passe o mouse aqui",
                 bg="#2E6DA4", fg="white",
                 font=("Arial", 11, "bold"),
                 relief=tk.FLAT, padx=20, pady=10, bd=0,
                 cursor="hand2")
btn1.pack(pady=10)
fazer_hover(btn1, "#2E6DA4", "#1E3A5F")

# — Botão 2: Hover com mudança de texto
btn2 = tk.Button(root, text="Excluir",
                 bg="#6B1A1A", fg="white",
                 font=("Arial", 11, "bold"),
                 relief=tk.FLAT, padx=20, pady=10, bd=0,
                 cursor="hand2")
btn2.pack(pady=10)
fazer_hover(btn2, "#6B1A1A", "#DC3545",
            texto_normal="Excluir", texto_hover="⚠️ Confirmar exclusão?")

# — Botão 3: Hover com mudança de fonte
btn3 = tk.Button(root, text="Hover me!",
                 bg="#28A745", fg="white",
                 font=("Arial", 11),
                 relief=tk.FLAT, padx=20, pady=10, bd=0,
                 cursor="hand2")
btn3.pack(pady=10)


def on_enter_btn3(e):
    btn3.configure(bg="#1A6B3C", font=("Arial", 12, "bold"))


def on_leave_btn3(e):
    btn3.configure(bg="#28A745", font=("Arial", 11, "normal"))


btn3.bind("<Enter>", on_enter_btn3)
btn3.bind("<Leave>", on_leave_btn3)

# — Label clicável com hover (link)
lbl_link = tk.Label(root, text="Clique aqui para mais informações",
                    fg="#2E6DA4", bg="#F4F6F9",
                    font=("Arial", 11, "underline"),
                    cursor="hand2")
lbl_link.pack(pady=10)

lbl_link.bind("<Enter>", lambda e: lbl_link.configure(fg="#DC3545"))
lbl_link.bind("<Leave>", lambda e: lbl_link.configure(fg="#2E6DA4"))

# — Botão com hover em cor diferente
btn4 = tk.Button(root, text="Sucesso",
                 bg="#17A2B8", fg="white",
                 font=("Arial", 11, "bold"),
                 relief=tk.FLAT, padx=20, pady=10, bd=0,
                 cursor="hand2")
btn4.pack(pady=10)
fazer_hover(btn4, "#17A2B8", "#0F6674")

root.mainloop()