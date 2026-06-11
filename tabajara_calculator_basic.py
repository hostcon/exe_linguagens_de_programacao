import tkinter as tk
from tkinter import messagebox


# ==========================================
# CALCULADORA TABAJARA 1.0
# ==========================================
# Versão simplificada para ensino de programação
# Operadores: + - X ÷ | Parênteses permitidos na digitação

# ==========================================
# FUNÇÕES DA CALCULADORA
# ==========================================

def adicionar(valor):
    """Adiciona o valor clicado ao display"""
    display.insert(tk.END, valor)


def limpar():
    """Limpa todo o display"""
    display.delete(0, tk.END)


def limpar_ultimo():
    """Apaga o último caractere (backspace)"""
    atual = display.get()
    if atual:
        display.delete(len(atual) - 1, tk.END)


def inverter_sinal():
    """Inverte o sinal do número atual"""
    try:
        valor = display.get()
        if valor:
            # Converte para número e inverte
            num = float(valor)
            display.delete(0, tk.END)
            display.insert(0, str(-num))
    except:
        pass  # Se não for número, ignora


def porcentagem():
    """Converte o valor para porcentagem"""
    try:
        valor = display.get()
        if valor:
            num = float(valor)
            display.delete(0, tk.END)
            display.insert(0, str(num / 100))
    except:
        pass


def calcular():
    """Calcula a expressão matemática"""
    try:
        expressao = display.get()

        if not expressao:
            return

        # Substitui símbolos visuais por operadores Python
        expressao = expressao.replace('X', '*')
        expressao = expressao.replace('÷', '/')

        # Calcula usando eval (ambiente seguro para sala de aula)
        resultado = eval(expressao)

        # Formata o resultado
        if isinstance(resultado, float):
            if resultado.is_integer():
                resultado = int(resultado)
            else:
                resultado = round(resultado, 8)

        # Exibe o resultado
        display.delete(0, tk.END)
        display.insert(0, str(resultado))

    except ZeroDivisionError:
        messagebox.showerror("Erro", "Não é possível dividir por zero!")
        limpar()
    except Exception:
        messagebox.showerror("Erro", "Expressão inválida!\nUse números e operadores ( ) + - X ÷")
        limpar()


# ==========================================
# JANELA PRINCIPAL
# ==========================================

janela = tk.Tk()
janela.title("Calculadora Tabajara 1.0")
janela.geometry("360x500")
janela.resizable(False, False)
janela.configure(bg='#1e1e1e')  # Fundo escuro

# ==========================================
# TÍTULO DA CALCULADORA (ACIMA DO DISPLAY)
# ==========================================

titulo = tk.Label(
    janela,
    text="Tabajara Calculator 1.0",
    font=("Arial", 12, "bold"),
    bg="#1e1e1e",
    fg="#ff9500"  # Laranja bonito
)
titulo.grid(row=0, column=0, columnspan=4, pady=(10, 5))

# ==========================================
# DISPLAY
# ==========================================

display = tk.Entry(
    janela,
    font=("Arial", 24, "bold"),
    justify="right",
    bd=10,
    relief="sunken",
    bg="#2d2d2d",
    fg="#ffffff"
)

display.grid(
    row=1,
    column=0,
    columnspan=4,
    padx=10,
    pady=(0, 10),
    sticky="nsew"
)

# ==========================================
# AVISO SOBRE PARÊNTESES
# ==========================================

aviso = tk.Label(
    janela,
    text="💡 Dica: Use parênteses na digitação: (2+3)*4",
    font=("Arial", 9),
    bg="#1e1e1e",
    fg="#888888"
)
aviso.grid(row=2, column=0, columnspan=4, pady=(0, 10))

# ==========================================
# CORES DOS BOTÕES
# ==========================================

cor_numero = "#333333"
cor_operador = "#ff9500"
cor_especial = "#5a5a5a"
cor_igual = "#2196f3"

# ==========================================
# BOTÕES (MATRIZ 5x4)
# ==========================================

botoes = [
    ['C', '⌫', '%', '÷'],
    ['7', '8', '9', 'X'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '.', '=']
]

# ==========================================
# CRIAÇÃO DOS BOTÕES
# ==========================================

for linha in range(len(botoes)):
    for coluna in range(len(botoes[linha])):

        texto = botoes[linha][coluna]

        # DEFINE A COR E O COMANDO DE CADA BOTÃO
        if texto == 'C':
            cor = cor_especial
            comando = limpar

        elif texto == '⌫':
            cor = cor_especial
            comando = limpar_ultimo

        elif texto == '%':
            cor = cor_especial
            comando = porcentagem

        elif texto == '=':
            cor = cor_igual
            comando = calcular

        elif texto in ['÷', 'X', '-', '+']:
            cor = cor_operador
            comando = lambda v=texto: adicionar(v)

        else:  # NÚMEROS E PONTO
            cor = cor_numero
            comando = lambda v=texto: adicionar(v)

        # CRIA O BOTÃO
        btn = tk.Button(
            janela,
            text=texto,
            font=("Arial", 18, "bold") if texto == '=' else ("Arial", 16),
            bg=cor,
            fg="white",
            bd=0,
            relief="flat",
            activebackground=cor,
            activeforeground="white",
            cursor="hand2",
            command=comando
        )

        # POSICIONA O BOTÃO NA GRADE
        if texto == '0':
            # Botão 0 ocupa 2 colunas
            btn.grid(
                row=linha + 3,  # +3 por causa do título, display e aviso
                column=coluna,
                columnspan=1,
                sticky="nsew",
                padx=2,
                pady=2
            )
        elif texto == '=':
            # Botão = na última coluna
            btn.grid(
                row=linha + 3,
                column=3,
                sticky="nsew",
                padx=2,
                pady=2
            )
        else:
            btn.grid(
                row=linha + 3,
                column=coluna,
                sticky="nsew",
                padx=2,
                pady=2
            )

# ==========================================
# CONFIGURAÇÃO DA GRADE (EXPANSÃO)
# ==========================================

# Configura as 4 colunas para expandirem igualmente
for i in range(4):
    janela.grid_columnconfigure(i, weight=1)

# Configura as linhas (título, display, aviso + 5 linhas de botões)
for i in range(8):  # 0 a 7 = 8 linhas
    janela.grid_rowconfigure(i, weight=1)

# ==========================================
# LOOP PRINCIPAL
# ==========================================

janela.mainloop()
