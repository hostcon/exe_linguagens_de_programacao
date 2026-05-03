from flask import Flask, render_template, request, jsonify
import sqlite3, random, bcrypt

app = Flask(__name__)

# =========================
# CONFIG RTP (ajustável)
# =========================
SIMBOLOS = ["🍊","🌰","🍵","🐂","⭐"]  # ordem importa
# pesos (mais comum → maior peso)
PESOS = [50, 30, 15, 4, 1]

# tabela de pagamento (3 iguais / 2 iguais)
PAGAMENTOS_3 = {
    "🍊": 4,
    "🌰": 6,
    "🍵": 10,
    "🐂": 25,
    "⭐": 80
}
PAGAMENTO_2 = 2  # dois iguais

CUSTO = 2

# =========================
# DB
# =========================
def db():
    return sqlite3.connect("slot.db")

with db() as conn:
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        saldo REAL)""")
    conn.commit()

# =========================
# HELPERS
# =========================
def sorteio():
    # weighted choice por rolo
    return random.choices(SIMBOLOS, weights=PESOS, k=3)

def calcular_premio(r):
    # 3 iguais
    if r[0] == r[1] == r[2]:
        return PAGAMENTOS_3[r[0]]
    # 2 iguais
    if len(set(r)) == 2:
        return PAGAMENTO_2
    return 0

# =========================
# ROTAS
# =========================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = data["user"]
    pwd = (data.get("pwd") or "").encode()

    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (user,))
        u = c.fetchone()

        if not u:
            return jsonify({"ok": False, "msg": "Usuário não existe"})

        # valida senha só se foi enviada (auto-login usa pwd vazio)
        if pwd:
            if not bcrypt.checkpw(pwd, u[1].encode()):
                return jsonify({"ok": False, "msg": "Senha incorreta"})

        return jsonify({"ok": True, "saldo": u[2]})

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

@app.route("/spin", methods=["POST"])
def spin():
    user = request.json["user"]

    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT saldo FROM users WHERE username=?", (user,))
        row = c.fetchone()
        if not row:
            return jsonify({"ok": False, "msg": "Usuário inválido"})

        saldo = row[0]
        if saldo < CUSTO:
            return jsonify({"ok": False, "msg": "Sem saldo"})

        saldo -= CUSTO

        r = sorteio()
        premio = calcular_premio(r)

        saldo += premio

        c.execute("UPDATE users SET saldo=? WHERE username=?", (saldo, user))
        conn.commit()

    return jsonify({"ok": True, "r": r, "saldo": saldo, "premio": premio})

@app.route("/ranking")
def ranking():
    with db() as conn:
        c = conn.cursor()
        c.execute("SELECT username, saldo FROM users ORDER BY saldo DESC LIMIT 10")
        return jsonify(c.fetchall())

if __name__ == "__main__":
    app.run(debug=True)