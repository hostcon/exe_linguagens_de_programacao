# CALCULADORA DE JUROS COMPOSTOS
print("=== Simulador de Investimento na Sicredi ===\n")

principal = float(input("Valor inicial (R$): "))
taxa = float(input("Taxa de juros ao mês (%): "))
tempo = int(input("Tempo em meses: "))

montante = principal * (1 + taxa/100) ** tempo
print(f"\nMontante final: R$ {montante:.2f}")