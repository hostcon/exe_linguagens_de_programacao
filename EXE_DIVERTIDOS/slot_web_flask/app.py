from flask import Flask, render_template, request, jsonify
import sqlite3, random

app = Flask(__name__)

SIMBOLOS = ["🍵","🌰","🐂","⭐","🍊"]
CUSTO = 2

def db():
    return sqlite3.connect("slot.db")

# cria tabelas
with db() as conn:
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, saldo REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS achievements (username TEXT, nome TEXT)")
    conn.commit()

# =====================
# ROTAS
# =====================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = data["user"]
    pwd = data["pwd"]

    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        u = c.fetchone()

        if u:
            if u[1] != pwd:
                return jsonify({"ok": False, "msg": "Senha incorreta"})
        else:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (user, pwd, 20))

        conn.commit()

        c.execute("SELECT saldo FROM users WHERE username=?", (user,))
        saldo = c.fetchone()[0]

    return jsonify({"ok": True, "saldo": saldo})

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

@app.route("/ranking")
def ranking():
    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT username, saldo FROM users ORDER BY saldo DESC LIMIT 10")
        data = c.fetchall()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)