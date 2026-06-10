import tkinter as tk
from tkinter import messagebox

# ==================== FUNÇÃO PRINCIPAL ====================
def adicionar(valor):
    display.insert(tk.END, valor)

def limpar():
    display.delete(0, tk.END)

def calcular():
    try:
        expressao = display.get()
        # Substitui o × e ÷ por operadores que o Python entende
        expressao = expressao.replace('×', '*').replace('÷', '/')
        
        resultado = eval(expressao)
        
        # Mostra o resultado
        display.delete(0, tk.END)
        display.insert(tk.END, str(resultado))
        
    except ZeroDivisionError:
        messagebox.showerror("Erro", "Divisão por zero!")
        limpar()
    except:
        messagebox.showerror("Erro", "Expressão inválida!")
        limpar()


# ====================== INTERFACE ======================
janela = tk.Tk()
janela.title("Calculadora")
janela.geometry("360x500")
janela.resizable(False, False)

# Display (único campo)
display = tk.Entry(janela, font=("Arial", 24), justify="right", bd=10, relief="sunken")
display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, ipadx=8, ipady=20)

# Botões
botoes = [
    'C', '±', '%', '÷',
    '7', '8', '9', '×',
    '4', '5', '6', '-',
    '1', '2', '3', '+',
    '0', '.', '='
]

# Cores
cor_numero = "#ffffff"
cor_operador = "#ff9500"
cor_especial = "#a6a6a6"

row = 1
col = 0

for botao in botoes:
    if botao == "=":
        btn = tk.Button(janela, text=botao, font=("Arial", 18, "bold"), 
                        bg=cor_operador, fg="white", height=2,
                        command=calcular)
        btn.grid(row=row, column=col, columnspan=2, padx=3, pady=3, sticky="nsew")
        col += 2
    elif botao == "0":
        btn = tk.Button(janela, text=botao, font=("Arial", 18), bg=cor_numero,
                        command=lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, columnspan=2, padx=3, pady=3, sticky="nsew")
        col += 2
    elif botao in '÷×-+':
        btn = tk.Button(janela, text=botao, font=("Arial", 18, "bold"), 
                        bg=cor_operador, fg="white",
                        command=lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        col += 1
    elif botao in 'C±%':
        btn = tk.Button(janela, text=botao, font=("Arial", 16), bg=cor_especial,
                        command=limpar if botao == 'C' else lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        col += 1
    else:
        btn = tk.Button(janela, text=botao, font=("Arial", 18), bg=cor_numero,
                        command=lambda v=botao: adicionar(v))
        btn.grid(row=row, column=col, padx=3, pady=3, sticky="nsew")
        col += 1
    
    if col > 3:
        col = 0
        row += 1

# Configurar peso das linhas e colunas
for i in range(4):
    janela.grid_columnconfigure(i, weight=1)
for i in range(1, 6):
    janela.grid_rowconfigure(i, weight=1)

janela.mainloop()