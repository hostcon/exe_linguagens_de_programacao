import sqlite3

# ==========================================
# PARTE 1: FUNÇÕES DE APOIO
# ==========================================

def verificar_aprovacao(nota_do_aluno):
    """Retorna o status baseado na nota."""
    if nota_do_aluno >= 7.0:
        return "Aprovado 🎓"
    elif nota_do_aluno >= 5.0:
        return "Recuperação 📚"
    else:
        return "Reprovado ❌"

def listar_alunos(cursor):
    # Pede ao banco de dados para selecionar todos os alunos
    cursor.execute("SELECT id, nome, nota FROM alunos")
    # O fetchall() pega todos os resultados e guarda na variável 'resultados'
    resultados = cursor.fetchall()
    
    if not resultados:
        print("\nNenhum aluno cadastrado no momento.")
    else:
        print("\n--- LISTA DE ALUNOS ---")
        # O for percorre cada linha que veio do banco de dados
        for linha in resultados:
            id_aluno = linha[0] # O id_aluno está na primeira posição (índice 0)
            nome = linha[1] # O nome está na segunda posição (índice 1)
            nota = linha[2] # A nota está na terceira posição (índice 2)
            status = verificar_aprovacao(nota)
            
            print(f"ID: {id_aluno} | Nome: {nome} | Nota: {nota} | Status: {status}")
        print("-----------------------")


# ==========================================
# PARTE 2: SETUP DO BANCO DE DADOS
# ==========================================
conexao = sqlite3.connect('escola.db')
cursor = conexao.cursor()

# Cria a tabela garantindo que cada aluno tenha um ID único (PRIMARY KEY)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        nota REAL NOT NULL
    )
''')
conexao.commit()


# ==========================================
# PARTE 3: O MENU PRINCIPAL (O CORAÇÃO DO SISTEMA)
# ==========================================
# O 'while True' mantém o programa rodando em loop até o usuário escolher Sair
while True:
    print("\n=== MENU DO SISTEMA ESCOLAR ===")
    print("1. Adicionar aluno e nota")
    print("2. Listar todos os alunos")
    print("3. Excluir um aluno")
    print("4. Sair do sistema")
    
    # Recebemos a escolha do usuário como texto mesmo (string)
    opcao = input("Escolha uma opção (1 a 4): ")
    
    # --- ROTEAMENTO DAS OPÇÕES COM IF / ELIF ---
    
    if opcao == '1':
        print("\n-- ADICIONAR ALUNO --")
        nome_novo = input("Digite o nome do aluno: ")
        nota_nova = float(input(f"Digite a nota de {nome_novo}: "))
        
        # Executa o comando de INSERIR no banco. 
        # Usamos (?) para proteger o banco e passamos as variáveis depois.
        cursor.execute("INSERT INTO alunos (nome, nota) VALUES (?, ?)", (nome_novo, nota_nova))
        conexao.commit()
        print(f"✅ Aluno {nome_novo} salvo com sucesso!")
        
    elif opcao == '2':
        # Chama a função que criamos lá em cima
        listar_alunos(cursor)
        
    elif opcao == '3':
        print("\n-- EXCLUIR ALUNO --")
        # Primeiro, mostramos a lista para o usuário saber qual ID excluir
        listar_alunos(cursor)
        
        id_excluir = input("\nDigite o ID do aluno que deseja excluir (ou '0' para cancelar): ")
        
        if id_excluir != '0':
            # Executa o comando SQL DELETE apontando para o ID escolhido
            cursor.execute("DELETE FROM alunos WHERE id = ?", (id_excluir,))
            conexao.commit()
            print("🗑️ Registro excluído com sucesso!")
            
    elif opcao == '4':
        print("\nEncerrando o sistema. Até a próxima!")
        break # O 'break' é o freio de mão que quebra o 'while True' e encerra o programa
        
    else:
        # Se o usuário digitar '5', 'A', ou qualquer coisa diferente
        print("\n⚠️ Opção inválida! Por favor, escolha um número de 1 a 4.")

# Fechando a conexão após sair do laço while
conexao.close()
