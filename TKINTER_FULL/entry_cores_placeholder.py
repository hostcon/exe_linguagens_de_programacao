import tkinter as tk

root = tk.Tk()
root.title("Entry com Cores e Placeholder")
root.configure(bg="#F4F6F9")
root.geometry("420x340")

# — Entry básico colorido
tk.Label(root, text="Entry com cores:", bg="#F4F6F9",
         font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(16,2))

entry_cor = tk.Entry(root,
                     fg="#1E3A5F",  # cor do texto
                     bg="#D6E8F7",  # fundo azul claro
                     insertbackground="#1E3A5F",  # cor do cursor (caret)
                     selectforeground="white",  # texto selecionado
                     selectbackground="#2E6DA4",  # fundo da seleção
                     font=("Arial", 12),
                     relief=tk.FLAT,
                     highlightthickness=2,
                     highlightcolor="#2E6DA4",  # borda ao focar
                     highlightbackground="#BBBBBB",  # borda sem foco
                     width=30)
entry_cor.pack(padx=20, pady=4, ipady=5)

# — Entry com placeholder
tk.Label(root, text="Entry com placeholder:", bg="#F4F6F9",
         font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(14,2))

PLACEHOLDER = "Digite seu e-mail..."
PLACEHOLDER_COLOR = "#AAAAAA"
TEXTO_COLOR = "#222222"

entry_ph = tk.Entry(root,
                    fg=PLACEHOLDER_COLOR,
                    bg="white",
                    font=("Arial", 12),
                    relief=tk.FLAT,
                    highlightthickness=2,
                    highlightcolor="#2E6DA4",
                    highlightbackground="#CCCCCC",
                    width=30)
entry_ph.insert(0, PLACEHOLDER)
entry_ph.pack(padx=20, pady=4, ipady=5)

def ao_focar(e):
    if entry_ph.get() == PLACEHOLDER:
        entry_ph.delete(0, tk.END)
        entry_ph.configure(fg=TEXTO_COLOR)

def ao_desfocar(e):
    if not entry_ph.get():
        entry_ph.insert(0, PLACEHOLDER)
        entry_ph.configure(fg=PLACEHOLDER_COLOR)

entry_ph.bind("<FocusIn>", ao_focar)
entry_ph.bind("<FocusOut>", ao_desfocar)

# — Text com cores e tags
tk.Label(root, text="Text com destaque:", bg="#F4F6F9",
         font=("Arial", 10, "bold")).pack(anchor="w", padx=20, pady=(14,2))

txt = tk.Text(root,
              fg="#1E1E2E", bg="white",
              insertbackground="#2E6DA4",
              selectbackground="#2E6DA4",
              font=("Courier New", 11),
              height=3, relief=tk.FLAT,
              highlightthickness=2,
              highlightcolor="#2E6DA4",
              highlightbackground="#CCCCCC")
txt.pack(padx=20, pady=4, fill=tk.X)

# Tags para colorir partes do texto
txt.tag_configure("erro", foreground="#DC3545", font=("Courier New", 11, "bold"))
txt.tag_configure("ok", foreground="#28A745", font=("Courier New", 11, "bold"))
txt.tag_configure("destaque", background="#FFF3CD")

txt.insert("1.0", "Status: ")
txt.insert(tk.END, "OK", "ok")
txt.insert(tk.END, " | Erro: ")
txt.insert(tk.END, "Campo vazio", "erro")

root.mainloop()