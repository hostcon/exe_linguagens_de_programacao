import tkinter as tk
from tkinter import messagebox


# ==========================================
# FUNÇÕES DA CALCULADORA - VERSÃO CORRIGIDA
# ==========================================

def adicionar(valor):
    """Adiciona valor ao display com validações (SEM DUPLICAÇÃO)"""
    atual = display.get()

    # LIMITE DE CARACTERES (evita display gigante)
    if len(atual) >= 35:
        return

    # ==========================================
    # TRATAMENTO ESPECIAL PARA PARÊNTESES
    # ==========================================
    if valor == '(':
        # Adiciona abertura de parêntese normalmente
        display.insert(tk.END, '(')
        return

    if valor == ')':
        # Verifica se há parêntese aberto antes de fechar
        if atual.count('(') > atual.count(')'):
            display.insert(tk.END, ')')
        return

    # ==========================================
    # TRATAMENTO DO PONTO DECIMAL
    # ==========================================
    if valor == '.':
        # Encontra o último número digitado
        import re
        numeros = re.findall(r'(\d+\.?\d*)', atual)
        if numeros:
            ultimo_numero = numeros[-1]
            if '.' in ultimo_numero:
                return  # Já tem ponto neste número

    # ==========================================
    # TRATAMENTO DE OPERADORES
    # ==========================================
    if valor in ['+', '-', 'X', '÷', '*', '/']:
        # Converte para símbolo visual
        if valor == '*':
            valor = 'X'
        elif valor == '/':
            valor = '÷'

        # Substitui operador consecutivo
        if atual and atual[-1] in ['+', '-', 'X', '÷', '*', '/', '(']:
            if atual[-1] in ['+', '-', 'X', '÷']:
                # Remove o último operador
                display.delete(len(atual) - 1, tk.END)

    # ==========================================
    # TRATAMENTO DE ZERO À ESQUERDA
    # ==========================================
    if valor.isdigit() and valor != '0':
        # Verifica se o display está vazio ou só tem zero
        if atual == '0':
            display.delete(0, tk.END)

    # ==========================================
    # PREVINE MÚLTIPLOS ZEROS NO INÍCIO
    # ==========================================
    if valor == '0' and atual == '0':
        return

    # ==========================================
    # PREVINE INSERIR OPERADOR ANTES DE NÚMERO
    # ==========================================
    if not atual and valor in ['+', '-', 'X', '÷']:
        if valor == '-':
            # Menos é permitido como sinal negativo
            display.insert(tk.END, valor)
        # Outros operadores não são permitidos no início
        return

    # INSERE O VALOR (SEM DUPLICAÇÃO!)
    display.insert(tk.END, valor)


def limpar():
    """Limpa completamente o display"""
    display.delete(0, tk.END)


def limpar_ultimo():
    """Apaga o último caractere"""
    atual = display.get()
    if atual:
        display.delete(len(atual) - 1, tk.END)


def inverter_sinal():
    """Inverte o sinal do último número"""
    try:
        expressao = display.get()
        if not expressao:
            return

        import re
        # Encontra o último número (incluindo negativo)
        numeros = re.findall(r'-?\d+\.?\d*', expressao)
        if not numeros:
            return

        ultimo_numero = numeros[-1]
        ultimo_pos = expressao.rfind(ultimo_numero)

        # Inverte sinal
        novo_numero = str(-float(ultimo_numero))

        # Remove .0 se for inteiro
        if novo_numero.endswith('.0'):
            novo_numero = novo_numero[:-2]

        # Substitui na expressão
        nova_expressao = expressao[:ultimo_pos] + novo_numero + expressao[ultimo_pos + len(ultimo_numero):]

        display.delete(0, tk.END)
        display.insert(0, nova_expressao)

    except:
        pass


def porcentagem():
    """Converte último número para porcentagem"""
    try:
        expressao = display.get()
        if not expressao:
            return

        import re
        # Encontra o último número
        numeros = re.findall(r'\d+\.?\d*', expressao)
        if not numeros:
            return

        ultimo_numero = numeros[-1]
        ultimo_pos = expressao.rfind(ultimo_numero)

        # Calcula porcentagem
        novo_numero = str(float(ultimo_numero) / 100)

        # Remove .0 se for inteiro
        if novo_numero.endswith('.0'):
            novo_numero = novo_numero[:-2]

        # Substitui
        nova_expressao = expressao[:ultimo_pos] + novo_numero + expressao[ultimo_pos + len(ultimo_numero):]

        display.delete(0, tk.END)
        display.insert(0, nova_expressao)

    except:
        pass


def calcular():
    """Calcula a expressão com suporte a parênteses"""
    try:
        expressao = display.get()

        if not expressao:
            return

        # Substitui símbolos visuais
        expressao = expressao.replace('X', '*')
        expressao = expressao.replace('÷', '/')

        # Remove operador no final (se houver)
        if expressao and expressao[-1] in '+-*/':
            expressao = expressao[:-1]

        # ==========================================
        # VERIFICA PARÊNTESES BALANCEADOS
        # ==========================================
        if expressao.count('(') != expressao.count(')'):
            messagebox.showerror("Erro", "Parênteses não balanceados!")
            return

        # AMBIENTE SEGURO
        ambiente = {
            '__builtins__': None,
            'abs': abs,
            'round': round,
            'float': float,
            'int': int,
            'pow': pow
        }

        # Verifica caracteres permitidos (incluindo parênteses)
        caracteres_permitidos = set('0123456789+-*/().% ')
        if not all(c in caracteres_permitidos for c in expressao):
            raise ValueError("Expressão contém caracteres inválidos")

        # CALCULA
        resultado = eval(expressao, ambiente, {})

        # FORMATA RESULTADO
        if isinstance(resultado, float):
            if resultado.is_integer():
                resultado = int(resultado)
            else:
                resultado = round(resultado, 10)
                # Remove trailing zeros
                resultado_str = str(resultado)
                if '.' in resultado_str:
                    resultado_str = resultado_str.rstrip('0').rstrip('.')
                    resultado = float(resultado_str) if '.' in resultado_str else int(float(resultado_str))

        display.delete(0, tk.END)
        display.insert(0, str(resultado))

    except ZeroDivisionError:
        messagebox.showerror("Erro", "Não é possível dividir por zero!")
        limpar()
    except SyntaxError as e:
        messagebox.showerror("Erro", f"Expressão inválida!\nVerifique a sintaxe")
        limpar()
    except Exception as e:
        messagebox.showerror("Erro", f"Expressão inválida!\n{str(e)}")
        limpar()


# ==========================================
# TECLADO FÍSICO
# ==========================================

def tecla_pressionada(event):
    """Lida com teclas do teclado físico"""
    tecla = event.char

    if tecla.isdigit() or tecla == '.':
        adicionar(tecla)
    elif tecla == '(':
        adicionar('(')
    elif tecla == ')':
        adicionar(')')
    elif tecla in ['+', '-']:
        adicionar(tecla)
    elif tecla == '*':
        adicionar('X')
    elif tecla == '/':
        adicionar('÷')
    elif tecla == '\r':  # Enter
        calcular()
    elif tecla == '\x08':  # Backspace
        limpar_ultimo()
    elif tecla in ['c', 'C']:
        limpar()
    elif tecla == '%':
        porcentagem()


# ==========================================
# JANELA PRINCIPAL
# ==========================================

janela = tk.Tk()
janela.title("Calculadora Tabajara - Com Parênteses")
janela.geometry("380x540")
janela.resizable(True, True)
janela.configure(bg='#1e1e1e')

# ==========================================
# DISPLAY
# ==========================================

display = tk.Entry(
    janela,
    font=("Arial", 24, "bold"),
    justify="right",
    bd=15,
    relief="sunken",
    bg="#2d2d2d",
    fg="#ffffff",
    insertbackground="white"
)

display.grid(
    row=0,
    column=0,
    columnspan=5,  # Agora tem 5 colunas para acomodar novos botões
    padx=15,
    pady=(15, 10),
    sticky="nsew"
)

# ==========================================
# LABEL INFORMATIVA
# ==========================================

label_info = tk.Label(
    janela,
    text="📐 Use parênteses: (  ) | Teclado físico suportado",
    font=("Arial", 9),
    bg="#1e1e1e",
    fg="#888888"
)
label_info.grid(row=1, column=0, columnspan=5, sticky="e", padx=15, pady=(0, 5))

# ==========================================
# CORES
# ==========================================

cor_numero = "#333333"
cor_numero_hover = "#4a4a4a"
cor_operador = "#ff9500"
cor_operador_hover = "#ffaa33"
cor_especial = "#5a5a5a"
cor_especial_hover = "#6e6e6e"
cor_igual = "#2196f3"
cor_igual_hover = "#42a5f5"
cor_parenteses = "#5856d6"  # Roxo para parênteses
cor_parenteses_hover = "#7371ee"

# ==========================================
# BOTÕES (NOVA MATRIZ 6x4 COM PARÊNTESES)
# ==========================================

botoes = [
    ['C', '⌫', '%', '÷'],
    ['7', '8', '9', 'X'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['0', '.', '(', ')'],  # Parênteses na linha 4
    ['=']  # Botão = isolado na linha 5
]


def on_enter(event, cor):
    event.widget.config(bg=cor)


def on_leave(event, cor_original):
    event.widget.config(bg=cor_original)


# ==========================================
# CRIAÇÃO DOS BOTÕES CORRIGIDA
# ==========================================

for linha in range(len(botoes)):
    for coluna in range(len(botoes[linha])):

        texto = botoes[linha][coluna]
        bg_cor = None
        fg_cor = "white"
        comando = None
        hover_cor = None

        # DEFINIÇÃO DOS BOTÕES
        if texto == 'C':
            bg_cor = cor_especial
            hover_cor = cor_especial_hover
            comando = limpar

        elif texto == '⌫':
            bg_cor = cor_especial
            hover_cor = cor_especial_hover
            comando = limpar_ultimo

        elif texto == '%':
            bg_cor = cor_especial
            hover_cor = cor_especial_hover
            comando = porcentagem

        elif texto == '=':
            bg_cor = cor_igual
            hover_cor = cor_igual_hover
            comando = calcular

        elif texto == '(' or texto == ')':
            bg_cor = cor_parenteses
            hover_cor = cor_parenteses_hover
            comando = lambda v=texto: adicionar(v)

        elif texto in ['÷', 'X', '-', '+']:
            bg_cor = cor_operador
            hover_cor = cor_operador_hover
            comando = lambda v=texto: adicionar(v)

        else:  # Números e ponto
            bg_cor = cor_numero
            hover_cor = cor_numero_hover
            comando = lambda v=texto: adicionar(v)

        # CRIA O BOTÃO
        font_style = ("Arial", 18, "bold") if texto == '=' else ("Arial", 16)

        btn = tk.Button(
            janela,
            text=texto,
            font=font_style,
            bg=bg_cor,
            fg=fg_cor,
            bd=0,
            relief="flat",
            activebackground=hover_cor,
            activeforeground="white",
            cursor="hand2",
            command=comando
        )

        # Efeito hover
        btn.bind("<Enter>", lambda e, c=hover_cor: on_enter(e, c))
        btn.bind("<Leave>", lambda e, c=bg_cor: on_leave(e, c))

        # POSICIONAMENTO ESPECIAL
        if texto == '0':
            # Botão 0 ocupa 2 colunas
            btn.grid(
                row=linha + 2,
                column=coluna,
                columnspan=1,
                sticky="nsew",
                padx=3,
                pady=3
            )
        elif texto == '=':
            # Botão = ocupa linha inteira na última linha
            btn.grid(
                row=linha + 2,
                column=0,
                columnspan=4,
                sticky="nsew",
                padx=3,
                pady=3,
                ipady=5
            )
        else:
            btn.grid(
                row=linha + 2,
                column=coluna,
                sticky="nsew",
                padx=3,
                pady=3
            )

# ==========================================
# CONFIGURAÇÃO DA GRID
# ==========================================

# Configura 4 colunas
for i in range(4):
    janela.grid_columnconfigure(i, weight=1)

# Configura linhas (display + label + 5 linhas de botões)
for i in range(7):  # 0 a 6 = 7 linhas
    janela.grid_rowconfigure(i, weight=1)

# Ajustes de peso
janela.grid_rowconfigure(0, weight=2)  # Display tem mais peso
janela.grid_rowconfigure(1, weight=0)  # Label fixo

# ==========================================
# BIND DO TECLADO
# ==========================================

janela.bind('<Key>', tecla_pressionada)

# ==========================================
# LOOP PRINCIPAL
# ==========================================

if __name__ == "__main__":
    janela.mainloop()
