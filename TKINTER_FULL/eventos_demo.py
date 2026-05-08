import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Eventos")

status = ttk.Label(root, text="Aguardando evento...", font=("Arial", 11))
status.pack(pady=16)

canvas = tk.Canvas(root, width=300, height=150, bg="white", cursor="crosshair")
canvas.pack(pady=8)

# Clique: event.x e event.y têm as coordenadas
canvas.bind("<Button-1>", lambda e: status.config(text=f"Clique em ({e.x}, {e.y})"))

# Duplo clique
canvas.bind("<Double-Button-1>", lambda e: (canvas.delete("all"), status.config(text="Canvas limpo")))

# Movimento do mouse
canvas.bind("<Motion>", lambda e: status.config(text=f"Mouse: ({e.x}, {e.y})"))

# Tecla na janela principal
root.bind("<KeyPress>", lambda e: status.config(text=f"Tecla: [{e.keysym}] char={e.char!r}"))

# Ctrl+S – salvar
root.bind("<Control-s>", lambda e: status.config(text="Ctrl+S pressionado – salvar!"))

# Escape – fechar
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()