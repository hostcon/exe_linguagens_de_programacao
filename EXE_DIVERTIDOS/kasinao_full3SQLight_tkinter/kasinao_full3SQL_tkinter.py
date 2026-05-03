import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import random
import pygame

# =========================
# DB (SQLite)
# =========================
conn = sqlite3.connect("slot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    saldo REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS achievements (
    username TEXT,
    nome TEXT
)
""")

conn.commit()

# =========================
# CONFIG
# =========================
SIMBOLOS = ["🍵", "🌰", "🐂", "⭐", "🍊"]
CUSTO = 2
usuario = None

# =========================
# AUDIO
# =========================
pygame.mixer.init()

def som(arq):
    try:
        pygame.mixer.Sound(arq).play()
    except:
        pass

# =========================
# LOGIN / CADASTRO
# =========================
def login():
    global usuario

    nome = simpledialog.askstring("Login", "Usuário:")
    senha = simpledialog.askstring("Senha", "Senha:", show="*")

    if not nome or not senha:
        return

    cursor.execute("SELECT * FROM users WHERE username=?", (nome,))
    user = cursor.fetchone()

    if user:
        if user[1] != senha:
            messagebox.showerror("Erro", "Senha incorreta!")
            return
    else:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (nome, senha, 20))
        conn.commit()

    usuario = nome
    atualizar_ui()

# =========================
# JOGO
# =========================
def get_saldo():
    cursor.execute("SELECT saldo FROM users WHERE username=?", (usuario,))
    return cursor.fetchone()[0]

def set_saldo(valor):
    cursor.execute("UPDATE users SET saldo=? WHERE username=?", (valor, usuario))
    conn.commit()

def atualizar_ui():
    saldo = get_saldo()
    saldo_label.config(text=f"{usuario} | R$ {saldo:.2f}")

def calcular(r):
    if r[0] == r[1] == r[2]:
        return 20, "🎉 JACKPOT"
    elif len(set(r)) == 2:
        return 5, "✨ Dois iguais"
    return 0, "😢 Nada"

def girar():
    if not usuario:
        messagebox.showwarning("Login", "Faça login!")
        return

    saldo = get_saldo()

    if saldo < CUSTO:
        resultado_label.config(text="Sem saldo!")
        return

    set_saldo(saldo - CUSTO)
    atualizar_ui()

    botao.config(state="disabled")
    som("sounds/spin.mp3")

    animar(15, 80)

def animar(n, delay):
    if n > 0:
        r = [random.choice(SIMBOLOS) for _ in range(3)]
        atualizar_slots(r)
        janela.after(delay, animar, n-1, delay+10)
    else:
        finalizar()

def atualizar_slots(r):
    slot1.config(text=r[0])
    slot2.config(text=r[1])
    slot3.config(text=r[2])

# =========================
# ACHIEVEMENTS
# =========================
def conquistar(nome):
    cursor.execute("SELECT * FROM achievements WHERE username=? AND nome=?", (usuario, nome))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO achievements VALUES (?, ?)", (usuario, nome))
        conn.commit()
        messagebox.showinfo("🏆 Conquista!", nome)

def verificar_conquistas(premio):
    saldo = get_saldo()

    if premio == 20:
        conquistar("💥 Primeiro Jackpot")

    if saldo >= 100:
        conquistar("💰 Rico!")

    if saldo <= 0:
        conquistar("💀 Quebrou")

# =========================
# FINALIZAÇÃO
# =========================
def finalizar():
    r = [slot1.cget("text"), slot2.cget("text"), slot3.cget("text")]
    premio, msg = calcular(r)

    saldo = get_saldo()

    if premio > 0:
        saldo += premio
        som("sounds/win.mp3")

    set_saldo(saldo)
    atualizar_ui()

    verificar_conquistas(premio)

    resultado_label.config(text=f"{msg} +{premio}" if premio else msg)
    botao.config(state="normal")

# =========================
# RANKING
# =========================
def ranking():
    cursor.execute("SELECT username, saldo FROM users ORDER BY saldo DESC LIMIT 10")
    dados = cursor.fetchall()

    texto = "🏆 Ranking\n\n"
    for i, (nome, saldo) in enumerate(dados, 1):
        texto += f"{i}. {nome} - R$ {saldo:.2f}\n"

    messagebox.showinfo("Ranking", texto)

# =========================
# UI
# =========================
janela = tk.Tk()
janela.title("🎰 Can’t Get Over SQLite")
janela.geometry("400x320")
janela.configure(bg="#1e1e1e")

tk.Label(janela, text="🎰 Ae Kasinão",
         font=("Arial", 18, "bold"),
         fg="#FFD700", bg="#1e1e1e").pack(pady=10)

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

resultado_label = tk.Label(janela, text="Faça login",
                           fg="white", bg="#1e1e1e")
resultado_label.pack(pady=10)

saldo_label = tk.Label(janela, text="",
                       fg="#00FFAA", bg="#1e1e1e",
                       font=("Arial", 12, "bold"))
saldo_label.pack()

botao = tk.Button(janela, text="🎰 GIRAR",
                  command=girar, bg="#FFD700")
botao.pack(pady=10)

frame_btn = tk.Frame(janela, bg="#1e1e1e")
frame_btn.pack()

tk.Button(frame_btn, text="Login", command=login).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Ranking", command=ranking).grid(row=0, column=1, padx=5)

janela.mainloop()