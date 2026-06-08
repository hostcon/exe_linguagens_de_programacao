
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
    ("João", 40),      # Primeiro aluno: nome João, nota 40
    ("Maria", 60),     # Segundo aluno: nome Maria, nota 60
    ("José", 94),      # Terceiro aluno: nome José, nota 94
    ("Pedro", 70),     # Quarto aluno: nome Pedro, nota 70
    ("Ricardo", 91),   # Quinto aluno: nome Ricardo, nota 91
    ("Bruno", 56),     # Sexto aluno: nome Bruno, nota 56
    ("Bruna", 54),     # Sétimo aluno: nome Bruna, nota 54
    ("Silas", 51),     # Oitavo aluno: nome Silas, nota 51
    ("Patrícia", 36),  # Nono aluno: nome Patrícia, nota 36
    ("Tatiana", 82),   # Décimo aluno: nome Tatiana, nota 82
    ("Roseane", 36),   # Décimo primeiro aluno: nome Roseane, nota 36
    ("Rebeca", 62),    # Décimo segundo aluno: nome Rebeca, nota 62
    ("Carlos", 65),    # Décimo terceiro aluno: nome Carlos, nota 65
    ("Marcos", 73),    # Décimo quarto aluno: nome Marcos, nota 73
    ("Adriana", 91),   # Décimo quinto aluno: nome Adriana, nota 91
    ("Adriano", 32),   # Décimo sexto aluno: nome Adriano, nota 32
]

# Usando a função "SE" genérica para avaliar a situação de um aluno específico

# Definindo a variável 'nota' com valor 60 (exemplo com a aluna Maria)
nota = 60

# Chamando a função 'se' com múltiplos níveis (aninhamento)
# Isso equivale à fórmula do Excel: =SE(nota>=70;"APROVADO";SE(nota>=50;"RECUPERAÇÃO";"REPROVADO"))
resultado = se(nota >= 70,           # Primeira condição: verifica se nota é maior ou igual a 70
               "APROVADO",           # Se a primeira condição for verdadeira, retorna "APROVADO"
               # Se a primeira condição for falsa (nota < 70), executa esta segunda parte:
               se(nota >= 50,        # Segunda condição: verifica se nota é maior ou igual a 50
                  "RECUPERAÇÃO",     # Se a segunda condição for verdadeira, retorna "RECUPERAÇÃO"
                  "REPROVADO"        # Se a segunda condição for falsa (nota < 50), retorna "REPROVADO"
               )
)

# Exibe o resultado no console
# Como a nota é 60:
# - 60 >= 70? Falso, então vai para o segundo SE
# - 60 >= 50? Verdadeiro, então retorna "RECUPERAÇÃO"
# O print mostrará: RECUPERAÇÃO
print(resultado)  # RECUPERAÇÃO
