# CONVERSOR DE PESO - MODO FAZENDEIRO
print("=== Conversor de Peso (Kg ↔ Arroba) ===\n")

peso = float(input("Digite o peso: "))
unidade = input("É em K (quilos) ou A (arrobas)? ").upper()

if unidade == "K":
    arrobas = peso / 15
    print(f"{peso} kg = {arrobas:.2f} arrobas")
elif unidade == "A":
    quilos = peso * 15
    print(f"{peso} arrobas = {quilos:.2f} kg")
else:
    print("Unidade inválida!")