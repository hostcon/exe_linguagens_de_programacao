from flask import Flask, render_template, request, jsonify
import sqlite3, random, bcrypt

app = Flask(__name__)

SIMBOLOS = ["🍵","🌰","🐂","⭐","🍊"]
CUSTO = 2

def db():
    return sqlite3.connect("slot.db")

# INIT DB
with db() as conn:
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        saldo REAL)""")

    c.execute("""CREATE TABLE IF NOT EXISTS achievements (
        username TEXT,
        nome TEXT)""")

    conn.commit()

# =====================
# ROTAS
# =====================
@app.route("/")
def index():
    return render_template("index.html")

# 🔐 LOGIN
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = data["user"]
    pwd = data["pwd"].encode()

    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        u = c.fetchone()

        if u:
            if pwd:  # só valida se senha foi enviada
                if not bcrypt.checkpw(pwd, u[1].encode()):
                    return jsonify({"ok": False, "msg": "Senha incorreta"})

        return jsonify({"ok": True, "saldo": u[2]})

# 🆕 CADASTRO
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = data["user"]
    pwd = data["pwd"].encode()

    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        if c.fetchone():
            return jsonify({"ok": False, "msg": "Usuário já existe"})

        hash_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt()).decode()

        c.execute("INSERT INTO users VALUES (?, ?, ?)", (user, hash_pwd, 20))
        conn.commit()

    return jsonify({"ok": True})

# 🎰 SPIN
@app.route("/spin", methods=["POST"])
def spin():
    user = request.json["user"]

    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT saldo FROM users WHERE username=?", (user,))
        saldo = c.fetchone()[0]

        if saldo < CUSTO:
            return jsonify({"ok": False, "msg": "Sem saldo"})

        saldo -= CUSTO

        r = [random.choice(SIMBOLOS) for _ in range(3)]

        premio = 0
        if r[0]==r[1]==r[2]:
            premio = 20
        elif len(set(r))==2:
            premio = 5

        saldo += premio

        c.execute("UPDATE users SET saldo=? WHERE username=?", (saldo, user))
        conn.commit()

    return jsonify({"ok": True, "r": r, "saldo": saldo, "premio": premio})

# 🏆 RANKING
@app.route("/ranking")
def ranking():
    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT username, saldo FROM users ORDER BY saldo DESC LIMIT 10")
        return jsonify(c.fetchall())

# =====================
if __name__ == "__main__":
    app.run(debug=True)