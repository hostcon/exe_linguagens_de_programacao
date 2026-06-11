def calcular_salario_liquido(salario_bruto):
    '''Calcula salário líquido com descontos INSS e IR simplificados'''
    if salario_bruto <= 1412:
        inss = salario_bruto * 0.075
    elif salario_bruto <= 2666.68:
        inss = salario_bruto * 0.09
    else:
        inss = salario_bruto * 0.12

    base_ir = salario_bruto - inss
    if base_ir <= 2112:
        ir = 0
    elif base_ir <= 2826.65:
        ir = base_ir * 0.075 - 158.40
    else:
        ir = base_ir * 0.15 - 370.40

    liquido = salario_bruto - inss - ir
    return liquido, inss, ir

nome = input("Nome do funcionário: ")
bruto = float(input("Salário bruto (R$): "))

liquido, inss, ir = calcular_salario_liquido(bruto)
print(f"\nHolerite de {nome}:")
print(f"  Salário bruto: R$ {bruto:>10.2f}")
print(f"  INSS:         -R$ {inss:>10.2f}")
print(f"  IR:           -R$ {ir:>10.2f}")
print(f"  Salário líquido: R$ {liquido:>8.2f}")
