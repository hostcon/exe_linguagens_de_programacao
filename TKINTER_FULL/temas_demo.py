import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

# Listar temas disponíveis na plataforma
print(style.theme_names())
# Windows: ("winnative", "clam", "alt", "default", "classic", "vista", "xpnative")
# macOS: ("aqua", "clam", "alt", "default", "classic")
# Linux: ("clam", "alt", "default", "classic")

# Aplicar um tema
style.theme_use("clam")  # mais moderno e cross-platform

root.mainloop()