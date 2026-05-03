import tkinter as tk
import random

# Configurações
simbolos = ["🍵", "🌰", "🐂", "⭐", "🍊"]
saldo = 20.0
custo_giro = 2

# Função de girar
def girar():
    global saldo

    if saldo < custo_giro:
        resultado_label.config(text="Saldo insuficiente!", fg="red")
        return

    saldo -= custo_giro

    resultado = [random.choice(simbolos) for _ in range(3)]

    # Atualiza os slots
    slot1.config(text=resultado[0])
    slot2.config(text=resultado[1])
    slot3.config(text=resultado[2])

    # Verifica vitória
    if resultado[0] == resultado[1] == resultado[2]:
        premio = 20
        saldo += premio
        resultado_label.config(text=f"🎉 JACKPOT! +R$ {premio}", fg="green")
    else:
        resultado_label.config(text="😢 Tente novamente...", fg="black")

    saldo_label.config(text=f"Saldo: R$ {saldo:.2f}")

# Janela principal
janela = tk.Tk()
janela.title("🎰 Máquina de Slots - Paraná")
janela.geometry("350x250")
janela.resizable(False, False)

# Título
titulo = tk.Label(janela, text="🎰 Slots Paraná", font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Frame dos slots
frame_slots = tk.Frame(janela)
frame_slots.pack(pady=10)

slot1 = tk.Label(frame_slots, text="❓", font=("Arial", 30))
slot1.pack(side="left", padx=10)

slot2 = tk.Label(frame_slots, text="❓", font=("Arial", 30))
slot2.pack(side="left", padx=10)

slot3 = tk.Label(frame_slots, text="❓", font=("Arial", 30))
slot3.pack(side="left", padx=10)

# Resultado
resultado_label = tk.Label(janela, text="Clique em GIRAR", font=("Arial", 12))
resultado_label.pack(pady=10)

# Saldo
saldo_label = tk.Label(janela, text=f"Saldo: R$ {saldo:.2f}", font=("Arial", 12, "bold"))
saldo_label.pack()

# Botão
botao = tk.Button(janela, text="GIRAR (R$2)", font=("Arial", 12), command=girar)
botao.pack(pady=15)

# Loop
janela.mainloop()