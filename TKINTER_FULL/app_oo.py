import tkinter as tk
from tkinter import ttk

class MeuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App em Classe")
        self.geometry("500x300")
        self._build_ui()  # monta a interface

    def _build_ui(self):
        """Cria e posiciona todos os widgets."""
        self.label = ttk.Label(self, text="Bem-vindo!")
        self.label.pack(expand=True)
        self.btn = ttk.Button(self, text="Sair", command=self.destroy)
        self.btn.pack(pady=8)

if __name__ == "__main__":
    app = MeuApp()
    app.mainloop()