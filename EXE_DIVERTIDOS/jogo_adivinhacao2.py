import random

# 10. JOGO DE ADIVINHAÇÃO
print("=== Adivinhe o Número ===\n")

secreto = random.randint(1, 100)
tentativas = 0
palpite = 0

while palpite != secreto:
    palpite = int(input("Seu palpite (1-100): "))
    tentativas += 1

    if palpite < secreto:
        print("Muito baixo!")
    elif palpite > secreto:
        print("Muito alto!")
    else:
        print(f"Parabéns! Acertou em {tentativas} tentativas!")