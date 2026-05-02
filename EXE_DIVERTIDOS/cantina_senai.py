# 9. LANCHONETE - CANTINA DO SENAI (Versão com Menu Numerado)

menu = {
    "coxinha": 7.50,
    "pastel": 8.00,
    "esfirra": 6.50,
    "pao de queijo": 2.50,
    "refrigerante": 5.00,
    "chimarrao": 4.00
}

# Converte o menu em lista numerada
itens_menu = list(menu.items())

print("=== Cantina do SENAI ===\n")
print("Cardápio:")
for i, (item, preco) in enumerate(itens_menu, 1):
    print(f"{i:2d} - {item.capitalize():<15} R$ {preco:.2f}")

total = 0.0
pedido = []

while True:
    try:
        escolha = input("\nDigite o número do item (ou 0 para sair): ").strip()

        if escolha == "0":
            break

        num = int(escolha)
        if 1 <= num <= len(itens_menu):
            item_escolhido = itens_menu[num - 1][0]  # nome do item
            preco = itens_menu[num - 1][1]

            qtd = int(input(f"Quantidade de {item_escolhido}: "))

            subtotal = preco * qtd
            total += subtotal
            pedido.append(f"{qtd}x {item_escolhido.capitalize()} - R$ {subtotal:.2f}")

            print(f"✅ {qtd}x {item_escolhido} adicionado!")
        else:
            print("Número inválido! Escolha um número do menu.")

    except ValueError:
        print("Por favor, digite um número válido.")

# Finaliza o pedido
print("\n" + "=" * 40)
print("=== SEU PEDIDO ===")
for item in pedido:
    print(item)
print("=" * 40)
print(f"Total a pagar: R$ {total:.2f}")
print("Obrigado pela preferência! 👋")