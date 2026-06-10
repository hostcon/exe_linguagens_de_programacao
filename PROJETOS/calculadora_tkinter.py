import tkinter as tk
from tkinter import messagebox

# ==================== FUNÇÕES DA CALCULADORA ====================

def adicionar(valor):
    """Adiciona um número ou operador no display."""
    display.insert(tk.END, valor)


def limpar():
    """Limpa completamente o display."""
    display.delete(0, tk.END)


def calcular():
    """Executa o cálculo da expressão digitada no display."""
    try:
        expressao = display.get()                    # Pega o texto atual do display
        
        # Substitui os símbolos bonitos por operadores que o Python entende
        expressao = expressao.replace('×', '*').replace('÷', '/')
        
        # eval() avalia a string como uma expressão matemática
        resultado = eval(expressao)
        
        # Limpa o display e mostra o resultado
        display.delete(0, tk.END)
        display.insert(tk.END, str(resultado))
        
    except ZeroDivisionError:
        messagebox.showerror("Erro", "Divisão por zero!")
        limpar()
    except:
        # Qualquer outro erro (parênteses errados, letras, etc.)
        messagebox.showerror("Erro", "Expressão inválida!")
        limpar()


# ====================== CRIAÇÃO DA INTERFACE ======================

janela = tk.Tk()
janela.title("Calculadora")
janela.geometry("360x500")      # Tamanho da janela (largura x altura)
janela.resizable(False, False)  # Impede redimensionar a janela

# ------------------- Display (campo único) -------------------
display = tk.Entry(
    janela, 
    font=("Arial", 24),           # Fonte grande
    justify="right",              # Alinha o texto à direita
    bd=10,                        # Espessura da borda
    relief="sunken"               # Estilo de borda afundada
)
# Posiciona o display na linha 0, ocupando as 4 colunas
display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipadx=8, ipady=20)


# ------------------- Lista de botões -------------------
botoes = [
    'C', '±', '%', '÷',     # Linha 1
    '7', '8', '9', '×',     # Linha 2
    '4', '5', '6', '-',     # Linha 3
    '1', '2', '3', '+',     # Linha 4
    '0', '.', '='           # Linha 5 (0 ocupa 2 colunas)
]

# Cores para deixar a calculadora mais bonita
cor_numero = "#ffffff"      # Branco para números
cor_operador = "#ff9500"    # Laranja para operadores
cor_especial = "#a6a6a6"    # Cinza para C, ±, %


# ------------------- Criação dos botões com Grid -------------------
row = 1   # Começa na linha 1 (linha 0 é o display)
col = 0   # Começa na coluna 0

for botao in botoes:
    
    if botao == "=":
        # Botão de igual ocupa 2 colunas e tem cor laranja
        btn = tk.Button(janela, text=botao, font=("Arial", 18, "bold"), 
                        bg=cor_operador, fg="white", height=2,
                        command=calcular)
        btn.grid(row=row, column=col, columnspan=2, padx=3, pady=3, sticky="nsew")
        col += 2
        
    elif botao == "0":
        # Botão 0 também ocupa 2 colunas
        btn = tk.Button(janela, text=botao, font=("Arial", 18), bg=cor_numero,
                        command=lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, columnspan=2, padx=3, pady=3, sticky="nsew")
        col += 2
        
    elif botao in '÷×-+':
        # Operadores matemáticos
        btn = tk.Button(janela, text=botao, font=("Arial", 18, "bold"), 
                        bg=cor_operador, fg="white",
                        command=lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        col += 1
        
    elif botao in 'C±%':
        # Botões especiais (C, ±, %)
        btn = tk.Button(janela, text=botao, font=("Arial", 16), bg=cor_especial,
                        command=limpar if botao == 'C' else lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        col += 1
        
    else:
        # Números normais (7,8,9,4,5,6,1,2,3)
        btn = tk.Button(janela, text=botao, font=("Arial", 18), bg=cor_numero,
                        command=lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        col += 1
    
    # Quando chegar no final da linha (4 colunas), pula para próxima linha
    if col > 3:
        col = 0
        row += 1


# ====================== CONFIGURAÇÃO DO GRID ======================

# Faz as colunas se expandirem igualmente quando a janela for redimensionada
for i in range(4):
    janela.grid_columnconfigure(i, weight=1)

# Faz as linhas (a partir da 1) se expandirem igualmente
# range(1, 6) porque temos 5 linhas de botões
for i in range(1, 6):
    janela.grid_rowconfigure(i, weight=1)


# Inicia o loop principal da interface
janela.mainloop()