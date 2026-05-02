# CALCULADORA BÁSICA
print("=== Calculadora Sulista ===\n")

num1 = float(input("Digite o primeiro número: "))
operador = input("Digite o operador (+ - * /): ")
num2 = float(input("Digite o segundo número: "))

if operador == "+":
    resultado = num1 + num2
elif operador == "-":
    resultado = num1 - num2
elif operador == "*":
    resultado = num1 * num2
elif operador == "/":
    if num2 == 0:
        print("Bah, não dá pra dividir por zero!")
        resultado = None
    else:
        resultado = num1 / num2
else:
    print("Operador inválido!")
    resultado = None

if resultado is not None:
    print(f"Resultado: {resultado}")