# CARRINHO DE COMPRAS
print("=== Carrinho da Feira ===\n")

total = 0
carrinho = []

while True:
    item = input("Item (ou 'sair' para finalizar): ").strip()
    if item.lower() == 'sair':
        break
    preco = float(input(f"Preço do {item}: R$ "))
    qtd = int(input("Quantidade: "))

    subtotal = preco * qtd
    total += subtotal
    carrinho.append(f"{qtd}x {item} - R$ {subtotal:.2f}")

print("\n=== Seu Carrinho ===")
for item in carrinho:
    print(item)
print(f"Total a pagar: R$ {total:.2f}")