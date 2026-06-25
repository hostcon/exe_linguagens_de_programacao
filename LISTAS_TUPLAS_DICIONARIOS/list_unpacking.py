# Lista original de informações
infos = [
    "João",
    "Paulo",
    "Brasil",
    "Desempregado",
    "Solteiro",
    "Ensino Superior",
    "25"
]

# Macete: desempacotando o primeiro, o segundo e o último item,
# ignorando todo o conteúdo do meio com *_
nome, sobrenome, *_, idade = infos

# Exibindo o resultado
print(f"{nome} {sobrenome} tem {idade} anos")

