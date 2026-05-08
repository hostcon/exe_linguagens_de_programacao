import tkinter as tk

root = tk.Tk()
root.title("Menu com Itens Dinâmicos")
root.geometry("400x300")

txt = tk.Text(root)
txt.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

menubar = tk.Menu(root)
root.config(menu=menubar)

menu_arq = tk.Menu(menubar, tearoff=0)
menu_arq.add_command(label="Novo")
menu_arq.add_command(label="Salvar", state=tk.DISABLED)
menubar.add_cascade(label="Arquivo", menu=menu_arq)

# Monitora o campo de texto
def ao_modificar(event=None):
    tem_conteudo = bool(txt.get("1.0", tk.END).strip())
    estado = tk.NORMAL if tem_conteudo else tk.DISABLED
    menu_arq.entryconfigure(1, state=estado)  # índice 1 = Salvar

txt.bind("<KeyRelease>", ao_modificar)

root.mainloop()