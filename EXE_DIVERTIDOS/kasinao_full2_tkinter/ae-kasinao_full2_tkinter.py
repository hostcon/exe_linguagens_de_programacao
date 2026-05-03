import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import pygame
import json
import os

# =========================
# CONFIG
# =========================
ARQ_USERS = "users.json"
SIMBOLOS = ["🍵", "🌰", "🐂", "⭐", "🍊"]
CUSTO = 2

# =========================
# AUDIO
# =========================
pygame.mixer.init()

def tocar_som(arq):
    try:
        pygame.mixer.Sound(arq).play()
    except:
        pass

def musica_fundo(play=True):
    try:
        if play:
            pygame.mixer.music.load("sounds/bg.mp3")
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()
    except:
        pass

def set_volume(v):
    pygame.mixer.music.set_volume(v)

# =========================
# USUÁRIOS
# =========================
def carregar_users():
    if os.path.exists(ARQ_USERS):
        with open(ARQ_USERS, "r") as f:
            return json.load(f)
    return {}

def salvar_users():
    with open(ARQ_USERS, "w") as f:
        json.dump(users, f, indent=4)

users = carregar_users()
usuario_atual = None

# =========================
# LOGIN
# =========================
def login():
    global usuario_atual

    nome = simpledialog.askstring("Login", "Digite seu usuário:")

    if not nome:
        return

    if nome not in users:
        users[nome] = {"saldo": 20}
        salvar_users()

    usuario_atual = nome
    atualizar_ui()

# =========================
# JOGO
# =========================
def atualizar_ui():
    saldo = users[usuario_atual]["saldo"]
    saldo_label.config(text=f"{usuario_atual} | Saldo: R$ {saldo:.2f}")

def calcular(resultado):
    if resultado[0] == resultado[1] == resultado[2]:
        return 20, "🎉 JACKPOT!"
    elif len(set(resultado)) == 2:
        return 5, "✨ Dois iguais!"
    return 0, "😢 Nada..."

def girar():
    if not usuario_atual:
        messagebox.showwarning("Login", "Faça login primeiro!")
        return

    saldo = users[usuario_atual]["saldo"]

    if saldo < CUSTO:
        resultado_label.config(text="Sem saldo!", fg="red")
        return

    users[usuario_atual]["saldo"] -= CUSTO
    atualizar_ui()
    salvar_users()

    botao.config(state="disabled")
    resultado_label.config(text="Girando...")

    tocar_som("sounds/spin.mp3")
    animar(15, 80)

def animar(rodadas, delay):
    if rodadas > 0:
        r = [random.choice(SIMBOLOS) for _ in range(3)]
        atualizar_slots(r)
        janela.after(delay, animar, rodadas-1, delay+10)
    else:
        finalizar()

def atualizar_slots(r):
    slot1.config(text=r[0])
    slot2.config(text=r[1])
    slot3.config(text=r[2])

def finalizar():
    r = [slot1.cget("text"), slot2.cget("text"), slot3.cget("text")]
    premio, msg = calcular(r)

    if premio > 0:
        users[usuario_atual]["saldo"] += premio
        tocar_som("sounds/win.mp3")

    salvar_users()
    atualizar_ui()

    resultado_label.config(text=f"{msg} +{premio}" if premio else msg)
    botao.config(state="normal")

# =========================
# RANKING
# =========================
def mostrar_ranking():
    ranking = sorted(users.items(), key=lambda x: x[1]["saldo"], reverse=True)

    texto = "🏆 Ranking:\n\n"
    for i, (nome, dados) in enumerate(ranking[:10], start=1):
        texto += f"{i}. {nome} - R$ {dados['saldo']:.2f}\n"

    messagebox.showinfo("Ranking", texto)

# =========================
# UI
# =========================
janela = tk.Tk()
janela.title("🎰 Can’t Get Over2")
janela.geometry("420x350")
janela.configure(bg="#1e1e1e")

titulo = tk.Label(janela, text="🎰 Ae Kasinão", font=("Arial", 18, "bold"),
                  fg="#FFD700", bg="#1e1e1e")
titulo.pack(pady=10)

frame = tk.Frame(janela, bg="#1e1e1e")
frame.pack()

def slot():
    return tk.Label(frame, text="❓", font=("Arial", 40),
                    bg="#000", fg="#00FFAA", width=2)

slot1 = slot()
slot2 = slot()
slot3 = slot()

slot1.pack(side="left", padx=10)
slot2.pack(side="left", padx=10)
slot3.pack(side="left", padx=10)

resultado_label = tk.Label(janela, text="Faça login para jogar",
                           fg="white", bg="#1e1e1e")
resultado_label.pack(pady=10)

saldo_label = tk.Label(janela, text="", fg="#00FFAA",
                       bg="#1e1e1e", font=("Arial", 12, "bold"))
saldo_label.pack()

botao = tk.Button(janela, text="🎰 GIRAR", command=girar, bg="#FFD700")
botao.pack(pady=10)

# =========================
# CONTROLES EXTRA
# =========================
frame_controles = tk.Frame(janela, bg="#1e1e1e")
frame_controles.pack(pady=10)

tk.Button(frame_controles, text="Login", command=login).grid(row=0, column=0, padx=5)
tk.Button(frame_controles, text="Ranking", command=mostrar_ranking).grid(row=0, column=1, padx=5)

# Volume
volume = tk.Scale(frame_controles, from_=0, to=1,
                  resolution=0.1, orient="horizontal",
                  label="Volume", command=lambda v: set_volume(float(v)))
volume.set(0.5)
volume.grid(row=1, column=0, columnspan=2)

# Mute
mutado = False
def toggle_mute():
    global mutado
    mutado = not mutado
    set_volume(0 if mutado else volume.get())

tk.Button(frame_controles, text="Mute", command=toggle_mute).grid(row=2, column=0, columnspan=2)

# Música fundo
musica_fundo(True)

janela.mainloop()