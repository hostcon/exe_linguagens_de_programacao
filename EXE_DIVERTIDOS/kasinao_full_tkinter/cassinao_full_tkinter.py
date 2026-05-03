import tkinter as tk
import random
import pygame
import os

# ==============================
# CONFIGURAÇÕES
# ==============================
simbolos = ["🍵", "🌰", "🐂", "⭐", "🍊"]
custo_giro = 2
arquivo_saldo = "saldo.txt"

# ==============================
# SOM
# ==============================
pygame.mixer.init()

def tocar_som(nome):
    try:
        pygame.mixer.Sound(nome).play()
    except:
        pass  # evita erro se não tiver arquivo

# ==============================
# SALDO (persistência)
# ==============================
def carregar_saldo():
    if os.path.exists(arquivo_saldo):
        with open(arquivo_saldo, "r") as f:
            return float(f.read())
    return 20.0

def salvar_saldo(valor):
    with open(arquivo_saldo, "w") as f:
        f.write(str(valor))

saldo = carregar_saldo()

# ==============================
# LÓGICA DE PRÊMIO
# ==============================
def calcular_premio(resultado):
    if resultado[0] == resultado[1] == resultado[2]:
        return 20, "🎉 JACKPOT!"
    elif len(set(resultado)) == 2:
        return 5, "✨ Dois iguais!"
    return 0, "😢 Nada..."

# ==============================
# ANIMAÇÃO
# ==============================
def animar_giro(rodadas=15, delay=80):
    if rodadas > 0:
        resultado = [random.choice(simbolos) for _ in range(3)]
        atualizar_slots(resultado)

        janela.after(delay, animar_giro, rodadas - 1, delay + 10)
    else:
        finalizar_giro()

def atualizar_slots(resultado):
    slot1.config(text=resultado[0])
    slot2.config(text=resultado[1])
    slot3.config(text=resultado[2])

# ==============================
# AÇÃO PRINCIPAL
# ==============================
def girar():
    global saldo

    if saldo < custo_giro:
        resultado_label.config(text="Saldo insuficiente!", fg="red")
        return

    saldo -= custo_giro
    salvar_saldo(saldo)
    saldo_label.config(text=f"Saldo: R$ {saldo:.2f}")

    botao.config(state="disabled")
    resultado_label.config(text="Girando...")

    tocar_som("sounds/spin.mp3")  # opcional

    animar_giro()

def finalizar_giro():
    global saldo

    resultado = [
        slot1.cget("text"),
        slot2.cget("text"),
        slot3.cget("text")
    ]

    premio, mensagem = calcular_premio(resultado)

    if premio > 0:
        saldo += premio
        tocar_som("sounds/ae-kasinao_2.mp3")  # opcional

    salvar_saldo(saldo)

    resultado_label.config(text=f"{mensagem} +R$ {premio}" if premio else mensagem)
    saldo_label.config(text=f"Saldo: R$ {saldo:.2f}")

    botao.config(state="normal")

# ==============================
# INTERFACE
# ==============================
janela = tk.Tk()
janela.title("🎰 Can’t Get Over")
janela.geometry("400x300")
janela.configure(bg="#1e1e1e")
janela.resizable(False, False)

# Título
titulo = tk.Label(
    janela,
    text="🎰 Ae Kasinão",
    font=("Helvetica", 18, "bold"),
    fg="#FFD700",
    bg="#1e1e1e"
)
titulo.pack(pady=10)

# Slots
frame_slots = tk.Frame(janela, bg="#1e1e1e")
frame_slots.pack(pady=10)

def criar_slot():
    return tk.Label(
        frame_slots,
        text="❓",
        font=("Arial", 40),
        bg="#000",
        fg="#00FFAA",
        width=2
    )

slot1 = criar_slot()
slot2 = criar_slot()
slot3 = criar_slot()

slot1.pack(side="left", padx=10)
slot2.pack(side="left", padx=10)
slot3.pack(side="left", padx=10)

# Resultado
resultado_label = tk.Label(
    janela,
    text="Clique em GIRAR",
    font=("Arial", 12),
    fg="white",
    bg="#1e1e1e"
)
resultado_label.pack(pady=10)

# Saldo
saldo_label = tk.Label(
    janela,
    text=f"Saldo: R$ {saldo:.2f}",
    font=("Arial", 12, "bold"),
    fg="#00FFAA",
    bg="#1e1e1e"
)
saldo_label.pack()

# Botão
botao = tk.Button(
    janela,
    text="🎰 GIRAR (R$2)",
    font=("Arial", 12, "bold"),
    bg="#FFD700",
    command=girar
)
botao.pack(pady=20)

# Rodar
janela.mainloop()