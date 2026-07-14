"""
Script opcional para popular o banco pdv.db com alguns produtos de exemplo.
Útil para testar o sistema ou demonstrar em sala de aula.

Uso:
    python seed_dados.py
"""

from database import Database

PRODUTOS_EXEMPLO = [
    # nome, codigo_barras, categoria, preco, estoque
    ("Caneta Esferográfica Azul", "7891000000010", "Papelaria", 2.50, 100),
    ("Caderno Universitário 10 Matérias", "7891000000027", "Papelaria", 24.90, 30),
    ("Refrigerante Lata 350ml", "7891000000034", "Bebidas", 5.00, 60),
    ("Água Mineral 500ml", "7891000000041", "Bebidas", 3.00, 80),
    ("Salgadinho 100g", "7891000000058", "Alimentos", 7.50, 40),
    ("Chocolate ao Leite 90g", "7891000000065", "Alimentos", 8.90, 25),
    ("Mouse USB Óptico", "7891000000072", "Informática", 39.90, 15),
    ("Pen Drive 32GB", "7891000000089", "Informática", 29.90, 20),
    ("Fone de Ouvido P2", "7891000000096", "Informática", 19.90, 18),
    ("Cabo USB-C 1m", "7891000000102", "Informática", 15.90, 22),
]


def main():
    db = Database()
    inseridos = 0
    for nome, codigo, categoria, preco, estoque in PRODUTOS_EXEMPLO:
        existente = db.buscar_produto_por_codigo(codigo)
        if existente:
            print(f"Já existe: {nome} (pulando)")
            continue
        db.inserir_produto(nome, codigo, categoria, preco, estoque)
        inseridos += 1
        print(f"Inserido: {nome}")
    print(f"\n{inseridos} produto(s) inserido(s) com sucesso.")
    db.fechar()


if __name__ == "__main__":
    main()
