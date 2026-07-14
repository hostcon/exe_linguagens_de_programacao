"""
Módulo de banco de dados do sistema PDV.
Gerencia a conexão com o SQLite e todas as operações de CRUD
(produtos, vendas e itens de venda).
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "pdv.db"


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.row_factory = sqlite3.Row
        self._criar_tabelas()

    def _criar_tabelas(self):
        cursor = self.conn.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_barras TEXT UNIQUE,
            nome TEXT NOT NULL,
            categoria TEXT,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT NOT NULL,
            total REAL NOT NULL,
            forma_pagamento TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        );
        """)
        self.conn.commit()

    # ---------------- PRODUTOS ----------------
    def listar_produtos(self, filtro=""):
        cursor = self.conn.cursor()
        if filtro:
            cursor.execute(
                "SELECT * FROM produtos WHERE nome LIKE ? OR codigo_barras LIKE ? ORDER BY nome",
                (f"%{filtro}%", f"%{filtro}%")
            )
        else:
            cursor.execute("SELECT * FROM produtos ORDER BY nome")
        return cursor.fetchall()

    def buscar_produto_por_codigo(self, codigo_barras):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE codigo_barras = ?", (codigo_barras,))
        return cursor.fetchone()

    def buscar_produto_por_id(self, produto_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
        return cursor.fetchone()

    def inserir_produto(self, nome, codigo_barras, categoria, preco, estoque):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO produtos (nome, codigo_barras, categoria, preco, estoque) VALUES (?, ?, ?, ?, ?)",
            (nome, codigo_barras or None, categoria, preco, estoque)
        )
        self.conn.commit()
        return cursor.lastrowid

    def atualizar_produto(self, produto_id, nome, codigo_barras, categoria, preco, estoque):
        cursor = self.conn.cursor()
        cursor.execute(
            """UPDATE produtos
               SET nome = ?, codigo_barras = ?, categoria = ?, preco = ?, estoque = ?
               WHERE id = ?""",
            (nome, codigo_barras or None, categoria, preco, estoque, produto_id)
        )
        self.conn.commit()

    def excluir_produto(self, produto_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        self.conn.commit()

    def atualizar_estoque(self, produto_id, quantidade_vendida):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
            (quantidade_vendida, produto_id)
        )
        self.conn.commit()

    # ---------------- VENDAS ----------------
    def registrar_venda(self, total, forma_pagamento, itens):
        """
        itens: lista de dicts com produto_id, nome_produto, quantidade,
        preco_unitario e subtotal (ver TabVenda.carrinho em main.py).
        """
        cursor = self.conn.cursor()
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO vendas (data_hora, total, forma_pagamento) VALUES (?, ?, ?)",
            (data_hora, total, forma_pagamento)
        )
        venda_id = cursor.lastrowid

        for item in itens:
            cursor.execute(
                """INSERT INTO itens_venda
                   (venda_id, produto_id, nome_produto, quantidade, preco_unitario, subtotal)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (venda_id, item["produto_id"], item["nome_produto"],
                 item["quantidade"], item["preco_unitario"], item["subtotal"])
            )
            self.atualizar_estoque(item["produto_id"], item["quantidade"])

        self.conn.commit()
        return venda_id

    def listar_vendas(self, data_inicio=None, data_fim=None):
        cursor = self.conn.cursor()
        if data_inicio and data_fim:
            cursor.execute(
                """SELECT * FROM vendas
                   WHERE date(data_hora) BETWEEN ? AND ?
                   ORDER BY data_hora DESC""",
                (data_inicio, data_fim)
            )
        else:
            cursor.execute("SELECT * FROM vendas ORDER BY data_hora DESC")
        return cursor.fetchall()

    def itens_da_venda(self, venda_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM itens_venda WHERE venda_id = ?", (venda_id,))
        return cursor.fetchall()

    def total_vendas_do_dia(self):
        cursor = self.conn.cursor()
        hoje = datetime.now().strftime("%Y-%m-%d")
        cursor.execute(
            "SELECT COALESCE(SUM(total), 0) as total FROM vendas WHERE date(data_hora) = ?",
            (hoje,)
        )
        return cursor.fetchone()["total"]

    def fechar(self):
        self.conn.close()
