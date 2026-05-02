import random

# JOGO DE ADIVINHAÇÃO
print("=== Adivinhe o Número (1 a 100) ===\n")

numero_secreto = random.randint(1, 100)
tentativas = 0
palpite = 0

while palpite != numero_secreto:
    palpite = int(input("Seu palpite: "))
    tentativas += 1

    if palpite < numero_secreto:
        print("Muito baixo! Tenta mais alto.")
    elif palpite > numero_secreto:
        print("Muito alto! Tenta mais baixo.")
    else:
        print(f"Acertou na mosca, bah! Em {tentativas} tentativas.")