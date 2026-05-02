import random

# 11. JOKENPÔ
print("=== Jokenpô - Pedra, Papel e Tesoura ===\n")

opcoes = ["pedra", "papel", "tesoura"]

while True:
    jogador = input("Escolha (pedra/papel/tesoura) ou 'sair': ").lower()
    if jogador == "sair":
        break
    if jogador not in opcoes:
        print("Escolha inválida!")
        continue

    pc = random.choice(opcoes)
    print(f"Computador escolheu: {pc}")

    if jogador == pc:
        print("Empate!")
    elif (jogador == "pedra" and pc == "tesoura") or \
         (jogador == "papel" and pc == "pedra") or \
         (jogador == "tesoura" and pc == "papel"):
        print("Você ganhou!")
    else:
        print("Computador ganhou!")