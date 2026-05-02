# CONVERSOR DE TEMPERATURA
print("=== Conversor de Temperatura ===\n")

temp = float(input("Digite a temperatura: "))
unidade = input("Está em C (Celsius) ou F (Fahrenheit)? ").upper()

if unidade == "C":
    fahrenheit = (temp * 9/5) + 32
    print(f"{temp}°C = {fahrenheit:.1f}°F")
    if temp < 10:
        print("Tá gelado pra caramba em Curitiba!")
elif unidade == "F":
    celsius = (temp - 32) * 5/9
    print(f"{temp}°F = {celsius:.1f}°C")
else:
    print("Unidade inválida!")