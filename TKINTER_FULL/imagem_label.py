import tkinter as tk

root = tk.Tk()
root.title("Imagem em Label")
root.geometry("400x300")

# Carrega PNG (suporte nativo – sem Pillow)
# A imagem DEVE estar no mesmo diretório do script
# Se não tiver a imagem, crie uma ou comente esta parte

try:
    img = tk.PhotoImage(file="logo.png")

    # Exibir somente imagem
    lbl_img = tk.Label(root, image=img)
    lbl_img.image = img  # OBRIGATÓRIO: manter referência
    lbl_img.pack(padx=20, pady=20)

    # Imagem + texto no mesmo Label
    lbl_combo = tk.Label(root,
                         image=img,
                         text="Meu Logo",
                         compound=tk.BOTTOM,  # texto abaixo
                         font=("Arial", 11, "bold"),
                         fg="#1E3A5F")
    lbl_combo.image = img
    lbl_combo.pack(padx=20, pady=8)

    # Redimensionar com subsample (divide) ou zoom (multiplica)
    # img_menor = img.subsample(2, 2)  # metade do tamanho
    # img_maior = img.zoom(2, 2)       # dobro do tamanho

except Exception as e:
    tk.Label(root, text=f"Imagem não encontrada:\n{str(e)}",
             fg="red", bg="white").pack(pady=50)

root.mainloop()