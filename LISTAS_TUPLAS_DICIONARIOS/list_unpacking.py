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

'''
Como funciona o truque?
nome, sobrenome: Capturam, respectivamente, os dois primeiros itens da lista ("João" e "Paulo") [00:15].

*_: O asterisco (*) diz ao Python para agrupar o restante dos elementos em uma lista, e o underline (_) é uma convenção na programação para indicar uma variável que será descartada (ignorada) [00:18].

idade: Como está posicionada após o *_, ela captura o último elemento da lista ("25") [00:24].
'''

