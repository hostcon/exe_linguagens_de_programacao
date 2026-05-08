import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# — Aplicação
root = tk.Tk()
root.title("App com Menu Completo")
root.geometry("700x460")

# Variáveis de estado
modo_escuro = tk.BooleanVar(value=False)
barra_status = tk.BooleanVar(value=True)
zoom_var = tk.StringVar(value="100%")

# — Área de trabalho
txt_area = tk.Text(root, font=("Courier New", 12), wrap=tk.WORD, undo=True)
txt_area.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

status_var = tk.StringVar(value="Pronto.")
status_bar = tk.Label(root, textvariable=status_var, relief=tk.SUNKEN, anchor="w")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# — Funções dos menus
def novo_arquivo():
    if txt_area.get("1.0", tk.END).strip():
        ok = messagebox.askyesno("Novo", "Descartar alterações?")
        if not ok:
            return
    txt_area.delete("1.0", tk.END)
    root.title("Sem título - App")
    status_var.set("Novo arquivo criado.")

def abrir_arquivo():
    caminho = filedialog.askopenfilename(
        filetypes=[("Texto", "*.txt"), ("Python", "*.py"), ("Todos", "*.*")])
    if caminho:
        with open(caminho, "r", encoding="utf-8") as f:
            txt_area.delete("1.0", tk.END)
            txt_area.insert("1.0", f.read())
        root.title(f"{caminho} - App")
        status_var.set(f"Aberto: {caminho}")

def salvar_arquivo():
    caminho = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
    if caminho:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(txt_area.get("1.0", tk.END))
        status_var.set(f"Salvo: {caminho}")

def alternar_modo_escuro():
    if modo_escuro.get():
        txt_area.configure(bg="#1E1E2E", fg="#CDD6F4", insertbackground="white")
        root.configure(bg="#1E1E2E")
        status_bar.configure(bg="#1E1E2E", fg="#CDD6F4")
    else:
        txt_area.configure(bg="white", fg="#1E1E2E", insertbackground="black")
        root.configure(bg="#F4F6F9")
        status_bar.configure(bg="#F4F6F9", fg="black")

def alternar_barra_status():
    if barra_status.get():
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    else:
        status_bar.pack_forget()

def mudar_zoom(valor):
    zoom_var.set(valor)
    tamanho = {"75%": 10, "100%": 12, "125%": 15, "150%": 18}
    txt_area.configure(font=("Courier New", tamanho.get(valor, 12)))
    status_var.set(f"Zoom: {valor}")

def sobre():
    messagebox.showinfo("Sobre", "Editor Simples\nPython 3 + Tkinter 8.6\nVersão 1.0")

# — Barra de menu
menubar = tk.Menu(root)
root.config(menu=menubar)

# — Menu Arquivo
menu_arquivo = tk.Menu(menubar, tearoff=0)
menu_arquivo.add_command(label="Novo", command=novo_arquivo, accelerator="Ctrl+N")
menu_arquivo.add_command(label="Abrir...", command=abrir_arquivo, accelerator="Ctrl+O")
menu_arquivo.add_command(label="Salvar...", command=salvar_arquivo, accelerator="Ctrl+S")
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=root.destroy, accelerator="Alt+F4")
menubar.add_cascade(label="Arquivo", menu=menu_arquivo)

# — Menu Editar
menu_editar = tk.Menu(menubar, tearoff=0)
menu_editar.add_command(label="Desfazer", command=lambda: txt_area.edit_undo(), accelerator="Ctrl+Z")
menu_editar.add_command(label="Refazer", command=lambda: txt_area.edit_redo(), accelerator="Ctrl+Y")
menu_editar.add_separator()
menu_editar.add_command(label="Copiar", command=lambda: root.event_generate("<<Copy>>"), accelerator="Ctrl+C")
menu_editar.add_command(label="Colar", command=lambda: root.event_generate("<<Paste>>"), accelerator="Ctrl+V")
menubar.add_cascade(label="Editar", menu=menu_editar)

# — Menu Exibir
menu_exibir = tk.Menu(menubar, tearoff=0)
menu_exibir.add_checkbutton(label="Modo Escuro", variable=modo_escuro, command=alternar_modo_escuro)
menu_exibir.add_checkbutton(label="Barra de Status", variable=barra_status, command=alternar_barra_status)
menu_exibir.add_separator()

# Submenu de zoom
submenu_zoom = tk.Menu(menu_exibir, tearoff=0)
for nivel in ["75%", "100%", "125%", "150%"]:
    submenu_zoom.add_radiobutton(label=nivel, variable=zoom_var, value=nivel,
                                  command=lambda n=nivel: mudar_zoom(n))
menu_exibir.add_cascade(label="Zoom", menu=submenu_zoom)
menubar.add_cascade(label="Exibir", menu=menu_exibir)

# — Menu Ajuda
menu_ajuda = tk.Menu(menubar, tearoff=0)
menu_ajuda.add_command(label="Sobre", command=sobre)
menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

# — Atalhos de teclado
root.bind("<Control-n>", lambda e: novo_arquivo())
root.bind("<Control-o>", lambda e: abrir_arquivo())
root.bind("<Control-s>", lambda e: salvar_arquivo())

root.mainloop()