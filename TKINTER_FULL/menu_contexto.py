import tkinter as tk

root = tk.Tk()
root.title("Menu de Contexto")
root.geometry("500x350")

txt = tk.Text(root, font=("Arial", 12), wrap=tk.WORD)
txt.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
txt.insert("1.0", "Clique com o botão DIREITO nesta área.\n")

# — Criação do menu de contexto
menu_ctx = tk.Menu(root, tearoff=0)  # tearoff=0 remove a linha pontilhada

menu_ctx.add_command(label="✂️ Recortar", command=lambda: txt.event_generate("<<Cut>>"))
menu_ctx.add_command(label="📋 Copiar", command=lambda: txt.event_generate("<<Copy>>"))
menu_ctx.add_command(label="📌 Colar", command=lambda: txt.event_generate("<<Paste>>"))
menu_ctx.add_separator()
menu_ctx.add_command(label="🔍 Selecionar Tudo", command=lambda: txt.tag_add(tk.SEL, "1.0", tk.END))
menu_ctx.add_separator()
menu_ctx.add_command(label="🗑️ Limpar Tudo", command=lambda: txt.delete("1.0", tk.END))

# — Exibir o menu nas coordenadas do clique
def exibir_menu_contexto(event):
    try:
        menu_ctx.tk_popup(event.x_root, event.y_root)
    finally:
        menu_ctx.grab_release()

# Vincula ao botão direito do mouse
# Windows/Linux: <Button-3> | macOS: <Button-2>
txt.bind("<Button-3>", exibir_menu_contexto)

root.mainloop()