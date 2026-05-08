import tkinter as tk

root = tk.Tk()
root.title("Canvas Demo")

canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(padx=10, pady=10)

# Retângulo (x1, y1, x2, y2)
canvas.create_rectangle(20, 20, 150, 100,
                        fill="#4A90C4", outline="#1E3A5F", width=2)

# Oval (elipse)
canvas.create_oval(200, 20, 380, 120,
                   fill="#28A745", outline="#1A6B3C", width=2)

# Linha
canvas.create_line(20, 150, 380, 150,
                   fill="red", width=3, dash=(10, 5))

# Texto no canvas
canvas.create_text(200, 200,
                   text="Canvas do Tkinter",
                   font=("Arial", 14, "bold"),
                   fill="#1E3A5F")

# Polígono (triângulo)
canvas.create_polygon(200, 230, 160, 290, 240, 290,
                      fill="#FFC107", outline="#8B4000", width=2)

root.mainloop()