import sqlite3

# ==========================================
# PARTE 1: DEFININDO AS NOSSAS FUNÇÕES
# ==========================================

def verificar_aprovacao(nota_do_aluno):
    """
    Função que recebe uma nota e retorna se o aluno passou ou não.
    Isso evita que a gente fique repetindo 'if/else' no código principal.
    """
    if nota_do_aluno >= 7.0:
        return "Aprovado 🎓"
    elif nota_do_aluno >= 5.0:
        return "Recuperação 📚"
    else:
        return "Reprovado ❌"


# ==========================================
# PARTE 2: CONEXÃO E CRIAÇÃO DO BANCO DE DADOS
# ==========================================

# 1. Cria o arquivo 'escola.db' e conecta a ele
conexao = sqlite3.connect('escola.db')

# 2. Cria o mensageiro (cursor)
cursor = conexao.cursor()

# 3. Executa o comando SQL para criar a tabela (se ela não existir)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nota REAL NOT NULL
    )
''')
# 4. Salva a criação da tabela
conexao.commit()


# ==========================================
# PARTE 3: USANDO O 'WHILE' PARA INSERIR DADOS
# ==========================================
print("=== SISTEMA DE CADASTRO ===")
print("Digite 'sair' no nome do aluno para encerrar.\n")

# O 'while True' cria um loop infinito que só para quando usamos o 'break'
while True:
    nome = input("Digite o nome do aluno: ")
    
    # Condição de parada do loop
    if nome.lower() == 'sair':
        print("Encerrando os cadastros...\n")
        break
    
    nota = float(input(f"Digite a nota de {nome}: "))
    
    # Executa o comando de INSERIR no banco. 
    # Usamos (?) para proteger o banco e passamos as variáveis depois.
    cursor.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome, nota))
    
    # Salva a inserção no banco de dados!
    conexao.commit()
    print(f"✅ Aluno {nome} salvo no banco de dados com sucesso!\n")


# ==========================================
# PARTE 4: USANDO O 'FOR' PARA LER OS DADOS
# ==========================================
print("=== RELATÓRIO DO BANCO DE DADOS ===")

# Pede ao banco de dados para selecionar todos os alunos
cursor.execute("SELECT nome, nota FROM alunos")

# O fetchall() pega todos os resultados e guarda na variável 'resultados'
resultados = cursor.fetchall()

# O 'for' vai passar por cada registro que veio do banco de dados
for linha in resultados:
    nome_banco = linha[0]  # O nome está na primeira posição (índice 0)
    nota_banco = linha[1]  # A nota está na segunda posição (índice 1)
    
    # Chamamos a nossa Função criada lá na Parte 1 para descobrir o status!
    status = verificar_aprovacao(nota_banco)
    
    print(f"Aluno: {nome_banco} | Nota: {nota_banco} | Situação: {status}")

# ==========================================
# PARTE 5: BOA PRÁTICA
# ==========================================
# Sempre fechar a conexão com o banco no final do programa
conexao.close()
