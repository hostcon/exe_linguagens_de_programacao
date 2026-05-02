# 13. PROGRAMA DE BANCO
saldo = 0.0

print("=== Banco Sicredi - Sua Conta ===\n")

while True:
    print("\n1. Depositar | 2. Sacar | 3. Ver Saldo | 4. Sair")
    op = input("Escolha: ")

    if op == "1":
        valor = float(input("Valor para depositar: R$ "))
        saldo += valor
        print(f"Depositado! Saldo atual: R$ {saldo:.2f}")
    elif op == "2":
        valor = float(input("Valor para sacar: R$ "))
        if valor <= saldo:
            saldo -= valor
            print(f"Saque realizado! Saldo atual: R$ {saldo:.2f}")
        else:
            print("Saldo insuficiente!")
    elif op == "3":
        print(f"Saldo atual: R$ {saldo:.2f}")
    elif op == "4":
        print("Obrigado por usar nosso banco!")
        break
    else:
        print("Opção inválida!")