# pip install Pillow
import tkinter as tk
from PIL import Image, ImageTk


class AppComBackground(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Background Responsivo")
        self.geometry("700x450")

        # Canvas de fundo
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Carrega imagem original (qualquer formato com Pillow)
        try:
            self._img_original = Image.open("background.jpg")
        except:
            # Se não tiver imagem, cria uma imagem colorida
            self._img_original = Image.new('RGB', (700, 450), color='#2E6DA4')

        self._bg_ref = None  # referencia para evitar GC

        # Detecta redimensionamento
        self.bind("<Configure>", self._ao_redimensionar)

        # Widgets sobre o canvas
        self._criar_conteudo()

    def _ao_redimensionar(self, event):
        """Redimensiona a imagem de fundo para cobrir a janela."""
        larg, alt = event.width, event.height
        if larg < 10 or alt < 10:
            return
        img = self._img_original.resize((larg, alt), Image.LANCZOS)
        self._bg_ref = ImageTk.PhotoImage(img)
        self.canvas.delete("background")
        self.canvas.create_image(0, 0, anchor="nw", image=self._bg_ref, tags="background")
        self.canvas.lower("background")  # sempre atrás

    def _criar_conteudo(self):
        """Adiciona widgets sobre o canvas."""
        frm = tk.Frame(self.canvas, bg="white", padx=24, pady=20, relief=tk.RIDGE)
        tk.Label(frm, text="Sistema", bg="white", font=("Arial", 16, "bold"),
                 fg="#1E3A5F").pack()
        tk.Label(frm, text="Bem-vindo ao sistema!", bg="white",
                 font=("Arial", 11)).pack(pady=8)
        tk.Button(frm, text="Entrar", bg="#2E6DA4", fg="white",
                  font=("Arial", 11), relief=tk.FLAT,
                  padx=20, pady=6).pack(pady=10)
        tk.Button(frm, text="Sair", command=self.destroy,
                  bg="#DC3545", fg="white", font=("Arial", 11),
                  relief=tk.FLAT, padx=20, pady=6).pack()

        self.canvas.create_window(350, 225, anchor="center", window=frm)


if __name__ == "__main__":
    AppComBackground().mainloop()