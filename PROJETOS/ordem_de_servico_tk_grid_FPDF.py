import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF

def gerar_pdf():
    # ========== OBTENDO DADOS DA INTERFACE ==========
    # Pega o texto digitado no campo "Cliente"
    cliente = entrada_cliente.get()
    
    # Pega o valor selecionado no combobox "Serviço"
    servico = combo_servico.get()
    
    # Pega o texto digitado no campo "Valor"
    valor = float(entrada_valor.get())

    # ========== VALIDAÇÃO DOS CAMPOS ==========
    # Verifica se algum campo está vazio (string vazia)
    if not cliente or not servico or not valor:
        # Exibe um aviso para o usuário
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return  # Sai da função sem gerar o PDF

    try:
        # ========== CRIAÇÃO DO OBJETO PDF ==========
        # Cria uma nova instância do FPDF
        # Parâmetros opcionais: orientation='P'(retrato) ou 'L'(paisagem), 
        # unit='mm', format='A4'
        pdf = FPDF()  # <-- OBS: tem um 'a' sobrando aqui no seu código (FPDF()a)
        
        # ========== ADICIONA UMA PÁGINA ==========
        # Cria uma nova página no documento PDF
        # O FPDF usa coordenadas em milímetros (mm)
        # - Margem esquerda padrão: 10mm
        # - Margem superior padrão: 10mm
        # - Página A4: 210mm x 297mm
        # - O cursor (posição atual) começa em (10, 10)
        pdf.add_page()
        
        # ========== DEFINE A FONTE ==========
        # set_font(família, estilo, tamanho)
        # - 'Arial': família da fonte (também pode ser 'Courier', 'Times', etc)
        # - estilo vazio ('') = normal (poderia ser 'B'=negrito, 'I'=itálico)
        # - size=12: tamanho da fonte em pontos (1pt = 1/72 polegada ≈ 0,35mm)
        pdf.set_font("Arial", size=12)

        # ========== 1ª CÉLULA: TÍTULO ==========
        # cell(largura, altura, texto, borda, quebra_linha, alinhamento, preenchimento)
        # 
        # pdf.cell(200, 10, txt="ORDEM DE SERVIÇO", ln=1, align="C")
        # 
        # POSICIONAMENTO NA PÁGINA:
        # ┌─────────────────────────────────────────────────────────────┐
        # │ (10, 10) ┌──────────────────────────────────────────┐     │
        # │          │        ORDEM DE SERVIÇO                │     │ ← 200mm largura
        # │          └──────────────────────────────────────────┘     │
        # │ (10, 20)                                                │
        # │                                                         │
        # └─────────────────────────────────────────────────────────────┘
        # 
        # PARÂMETROS:
        # - 200: largura em mm (200mm ocupa quase toda página)
        # - 10: altura em mm (10mm de altura)
        # - txt="ORDEM DE SERVIÇO": texto a ser exibido
        # - ln=1: após esta célula, pula para PRÓXIMA LINHA
        #   * ln=0: continua na mesma linha (à direita)
        #   * ln=1: vai para o início da próxima linha
        #   * ln=2: pula 2 linhas
        # - align="C": alinhamento CENTRALIZADO
        #   * 'L' = esquerda (left)
        #   * 'C' = centro (center)  
        #   * 'R' = direita (right)
        pdf.cell(200, 10, txt="ORDEM DE SERVIÇO", ln=1, align="C")
        
        # ========== PULA UMA LINHA EM BRANCO ==========
        # ln(10) - Adiciona um espaço vertical de 10mm
        # Isso cria um espaçamento entre o título e os dados
        # O cursor vai para (10, 30) - 10mm abaixo da posição atual
        # 
        # POSICIONAMENTO:
        # ┌─────────────────────────────────────────────────────────────┐
        # │ (10, 10) ┌──────────────────────────────────────────┐     │
        # │          │        ORDEM DE SERVIÇO                │     │
        # │          └──────────────────────────────────────────┘     │
        # │ (10, 20)                                                │
        # │          ← 10mm de espaço em branco (pdf.ln(10))       │
        # │ (10, 30) ┌──────────────────────────────────────────┐     │ ← Próximo texto aqui
        # │          │                                        │     │
        # └─────────────────────────────────────────────────────────────┘
        pdf.ln(10)

        # ========== 2ª CÉLULA: CLIENTE ==========
        # pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=1)
        # 
        # Exibe o nome do cliente com o rótulo "Cliente:"
        # - ln=1: após exibir, pula para próxima linha
        # - align não especificado: usa 'L' (esquerda) por padrão
        # 
        # POSICIONAMENTO: começa em (10, 30) e vai até (210, 40)
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=1)

        # ========== 3ª CÉLULA: SERVIÇO ==========
        # pdf.cell(200, 10, txt=f"Servico: {servico}", ln=1)
        # 
        # Exibe o serviço selecionado
        # - ln=1: após exibir, pula para próxima linha
        # - O cursor agora está em (10, 50)
        pdf.cell(200, 10, txt=f"Servico: {servico}", ln=1)

        # ========== 4ª CÉLULA: VALOR ==========
        # pdf.cell(200, 10, txt=f"Valor: R$ {valor}", ln=1)
        # 
        # Exibe o valor com formatação de moeda
        # - ln=1: após exibir, pula para próxima linha
        pdf.cell(200, 10, txt=f"Valor: R$ {valor}", ln=1)

        # ========== SALVA O ARQUIVO PDF ==========
        # Gera o arquivo PDF no disco
        # - O arquivo será salvo na mesma pasta do script
        # - Se o arquivo já existir, será sobrescrito
        pdf.output("ordem_de_servico.pdf")
        
        # Exibe mensagem de sucesso para o usuário
        messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")
        
    except Exception as e:
        # Se ocorrer qualquer erro, exibe mensagem de erro
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

# ========== CRIAÇÃO DA INTERFACE GRÁFICA (Tkinter) ==========

# Cria a janela principal
janela = tk.Tk()

# Define o título da janela
janela.title("Gerador de Ordem de Serviço")

# Define o tamanho da janela: 350px largura x 220px altura
janela.geometry("350x220")

# ========== CAMPO: CLIENTE ==========
# Cria um rótulo (label) com o texto "Cliente:"
# - grid(row=0, column=0): posiciona na linha 0, coluna 0
# - sticky="w": alinha à esquerda (west)
# - padx=10, pady=5: espaçamento externo de 10px horizontal e 5px vertical
tk.Label(janela, text="Cliente:").grid(row=0, column=0, sticky="w", padx=10, pady=5)

# Cria um campo de entrada de texto para o cliente
# - width=28: largura de 28 caracteres
entrada_cliente = tk.Entry(janela, width=28)
entrada_cliente.grid(row=0, column=1, padx=10, pady=5)

# ========== CAMPO: SERVIÇO ==========
# Cria um rótulo com o texto "Serviço:"
tk.Label(janela, text="Serviço:").grid(row=1, column=0, sticky="w", padx=10, pady=5)

# Lista de opções de serviços disponíveis
servicos = [
    "Formatação de Computador",
    "Instalação de Windows",
    "Manutenção de Rede",
    "Criação de Site",
    "Suporte Técnico"
]

# Cria um Combobox (menu suspenso) com as opções de serviço
# - values=servicos: lista de opções
# - width=26: largura de 26 caracteres
# - state="readonly": usuário não pode digitar, só selecionar
combo_servico = ttk.Combobox(janela, values=servicos, width=26, state="readonly")
combo_servico.grid(row=1, column=1, padx=10, pady=5)

# Define o primeiro item da lista como selecionado por padrão
combo_servico.current(0)  # Índice 0 = "Formatação de Computador"

# ========== CAMPO: VALOR ==========
# Cria um rótulo com o texto "Valor (R$):"
tk.Label(janela, text="Valor (R$):").grid(row=2, column=0, sticky="w", padx=10, pady=5)

# Cria um campo de entrada para o valor
entrada_valor = tk.Entry(janela, width=28)
entrada_valor.grid(row=2, column=1, padx=10, pady=5)

# ========== BOTÃO: GERAR PDF ==========
# Cria um botão que chama a função gerar_pdf() quando clicado
# - bg="green": fundo verde
# - fg="white": texto branco
# - columnspan=2: ocupa 2 colunas (centralizado)
botao_pdf = tk.Button(janela, text="Gerar PDF", command=gerar_pdf, bg="green", fg="white")
botao_pdf.grid(row=3, column=0, columnspan=2, pady=15)

# ========== INICIA O LOOP DA INTERFACE ==========
# Mantém a janela aberta e processa eventos (cliques, teclas, etc)
janela.mainloop()
