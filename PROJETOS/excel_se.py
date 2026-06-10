# Definição de uma função chamada "se" que imita a função SE do Excel
# Parâmetros:
# - condicao: uma expressão que será avaliada como verdadeira ou falsa
# - valor_se_verdadeiro: valor retornado se a condição for True
# - valor_se_falso: valor retornado se a condição for False
def se(condicao, valor_se_verdadeiro, valor_se_falso):
    # O return devolve o resultado da expressão ternária
    # Expressão ternária: (valor_se_verdadeiro if condicao else valor_se_falso)
    # Funciona assim:
    # - Se condicao for True, retorna valor_se_verdadeiro
    # - Se condicao for False, retorna valor_se_falso
    return valor_se_verdadeiro if condicao else valor_se_falso


# Dados dos alunos (já com as notas da sua tabela)
# Criando uma lista de tuplas, onde cada tupla contém (nome_do_aluno, nota)
alunos = [
    ("João", 40),  # Primeiro aluno: nome João, nota 40
    ("Maria", 60),  # Segundo aluno: nome Maria, nota 60
    ("José", 94),  # Terceiro aluno: nome José, nota 94
    ("Pedro", 70),  # Quarto aluno: nome Pedro, nota 70
    ("Ricardo", 91),  # Quinto aluno: nome Ricardo, nota 91
    ("Bruno", 56),  # Sexto aluno: nome Bruno, nota 56
    ("Bruna", 54),  # Sétimo aluno: nome Bruna, nota 54
    ("Silas", 51),  # Oitavo aluno: nome Silas, nota 51
    ("Patrícia", 36),  # Nono aluno: nome Patrícia, nota 36
    ("Tatiana", 82),  # Décimo aluno: nome Tatiana, nota 82
    ("Roseane", 36),  # Décimo primeiro aluno: nome Roseane, nota 36
    ("Rebeca", 62),  # Décimo segundo aluno: nome Rebeca, nota 62
    ("Carlos", 65),  # Décimo terceiro aluno: nome Carlos, nota 65
    ("Marcos", 73),  # Décimo quarto aluno: nome Marcos, nota 73
    ("Adriana", 91),  # Décimo quinto aluno: nome Adriana, nota 91
    ("Adriano", 32),  # Décimo sexto aluno: nome Adriano, nota 32
]

# Imprimindo o cabeçalho da tabela
# {:^15} centraliza o texto em 15 espaços
# {:^6} centraliza o texto em 6 espaços
# {:^12} centraliza o texto em 12 espaços
print(f"{'Aluno':^15} {'Nota':^6} {'Situação':^12}")
print("-" * 38)  # Imprime uma linha de separação com 38 traços

# Usando o loop FOR para processar CADA aluno individualmente
# O loop vai repetir o bloco de código para cada tupla dentro da lista 'alunos'
for nome, nota in alunos:  # Para cada aluno, pegue o 'nome' e a 'nota'

    # Aplicando a função SE aninhada para calcular a situação do aluno atual
    # Isso equivale a arrastar a fórmula no Excel para cada linha
    situacao = se(nota >= 70,  # Primeira condição: verifica se nota é maior ou igual a 70
                  "APROVADO",  # Se a primeira condição for verdadeira, retorna "APROVADO"
                  # Se a primeira condição for falsa (nota < 70), executa esta segunda parte:
                  se(nota >= 50,  # Segunda condição: verifica se nota é maior ou igual a 50
                     "RECUPERAÇÃO",  # Se a segunda condição for verdadeira, retorna "RECUPERAÇÃO"
                     "REPROVADO"  # Se a segunda condição for falsa (nota < 50), retorna "REPROVADO"
                     )
                  )

    # Exibe o resultado formatado para o aluno atual
    # {:15} alinha à esquerda com 15 espaços
    # {:>6} alinha à direita com 6 espaços (útil para números)
    # {:^12} centraliza com 12 espaços
    print(f"{nome:15} {nota:>6} {situacao:^12}")

print("-" * 38)  # Linha final para fechar a tabela

# Opcional: Contar quantos alunos em cada situação
print("\n--- RESUMO FINAL ---")
# Inicializa os contadores
aprovados = 0
recuperacao = 0
reprovados = 0

# Segundo loop FOR para contar as situações
for nome, nota in alunos:
    situacao = se(nota >= 70, "APROVADO", se(nota >= 50, "RECUPERAÇÃO", "REPROVADO"))

    # Incrementa o contador de acordo com a situação
    if situacao == "APROVADO":
        aprovados += 1  # aprovados = aprovados + 1
    elif situacao == "RECUPERAÇÃO":
        recuperacao += 1  # recuperacao = recuperacao + 1
    else:
        reprovados += 1  # reprovados = reprovados + 1

# Exibe o resumo
print(f"Total de APROVADOS: {aprovados}")
print(f"Total em RECUPERAÇÃO: {recuperacao}")
print(f"Total de REPROVADOS: {reprovados}")