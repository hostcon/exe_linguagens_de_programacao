import random

# 12. ROLADOR DE DADOS
print("=== Rolador de Dados ===\n")

qtd = int(input("Quantos dados quer rolar? "))

soma = 0
for i in range(qtd):
    dado = random.randint(1, 6)
    soma += dado
    print(f"Dado {i+1}: {dado}")

print(f"\nTotal: {soma}")