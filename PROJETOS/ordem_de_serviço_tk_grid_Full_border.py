import tkinter as tk
from tkinter import ttk, messagebox
from fpdf import FPDF
from datetime import datetime
import locale

# Configura o locale para o formato BRL (Real Brasileiro)
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8') # Linux
except:
    locale.setlocale(locale.LC_ALL, 'ptb') # Windows

# Variável global para o número da OS
numero_os = 1

def gerar_pdf():
    global numero_os
    cliente = entrada_cliente.get()
    servico = combo_servico.get()
    descricao = entrada_descricao.get("1.0", tk.END).strip()
    valor = entrada_valor.get()
    data = datetime.now().strftime("%d/%m/%Y")

    if not cliente or not servico or not valor:
        messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios!")
        return

    try:
        # Formata o valor no padrão BRL (R$ 1.234,56)
        valor_float = float(valor)
        valor_formatado = locale.currency(valor_float, grouping=True, symbol=True)

        # Cria o PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)

        # ===== HEADER =====
        pdf.set_fill_color(240, 240, 240)  # Cinza claro
        pdf.cell(0, 15, txt="ORDEM DE SERVIÇO", ln=1, align='C', fill=True)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, txt=f"Nº {numero_os:04d} | Data: {data}", ln=1, align='C')
        pdf.ln(5)

        # ===== LINHA DE GRADE =====
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(10)

        # ===== DADOS DO CLIENTE =====
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, txt=" DADOS DO CLIENTE ", ln=1, align='L', fill=True)
        pdf.set_font('Arial', size=12)
        pdf.cell(40, 10, txt="Cliente:", border=1)
        pdf.cell(150, 10, txt=cliente, border=1, ln=1)
        pdf.ln(5)

        # ===== DADOS DO SERVIÇO =====
        pdf.set_font('Arial', 'B', 12)
        pdf.set_fill_color(230, 230, 230)
        pdf.cell(0, 10, txt=" DADOS DO SERVIÇO ", ln=1, align='L', fill=True)
        pdf.set_font('Arial', size=12)

        # Linha com larguras fixas para evitar quebra de grade
        pdf.cell(40, 10, txt="Serviço:", border=1)  # 40px
        pdf.cell(100, 10, txt=servico, border=1)     # 100px
        pdf.cell(20, 10, txt="Valor:", border=1)     # 20px
        pdf.cell(30, 10, txt=valor_formatado, border=1, ln=1)  # 30px (FIXO)

        # Descrição (multilinha)
        pdf.cell(40, 10, txt="Descrição:", border=1)
        pdf.multi_cell(150, 10, txt=descricao if descricao else "N/A", border=1, ln=1)

        # ===== LINHA DE GRADE (RODAPÉ) =====
        pdf.ln(10)
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)

        # ===== ASSINATURA =====
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, txt="ASSINATURA", ln=1, align='L')
        pdf.set_font('Arial', size=10)
        pdf.cell(0, 10, txt="_________________________", ln=1, align='L')
        pdf.cell(0, 10, txt="Responsável: Wagner Rodrigues", ln=1, align='L')

        # Salva o PDF
        pdf.output(f"ordem_de_servico_{numero_os:04d}.pdf")
        numero_os += 1
        messagebox.showinfo("Sucesso", f"PDF gerado: ordem_de_servico_{numero_os-1:04d}.pdf")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

# ===== INTERFACE TKINTER =====
janela = tk.Tk()
janela.title("Gerador de Ordem de Serviço - Profissional")
janela.geometry("500x400")

# Cliente
tk.Label(janela, text="Cliente:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
entrada_cliente = tk.Entry(janela, width=50)
entrada_cliente.grid(row=0, column=1, padx=10, pady=5)

# Serviço
tk.Label(janela, text="Serviço:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
servicos = [
    "Formatação de Computador",
    "Instalação do Windows",
    "Manutenção de Rede",
    "Criação de Site",
    "Suporte Técnico",
    "Limpeza de Hardware",
    "Configuração de Servidor"
]
combo_servico = ttk.Combobox(janela, width=47, values=servicos, state="readonly")
combo_servico.grid(row=1, column=1, padx=10, pady=5)

# Descrição
tk.Label(janela, text="Descrição:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.NW)
entrada_descricao = tk.Text(janela, width=40, height=4)
entrada_descricao.grid(row=2, column=1, padx=10, pady=5)

# Valor
tk.Label(janela, text="Valor (R$):").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
entrada_valor = tk.Entry(janela, width=20)
entrada_valor.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

# Botão
botao_pdf = tk.Button(
    janela,
    text="Gerar PDF Profissional",
    command=gerar_pdf,
    bg="#2E8B57",
    fg="white",
    font=('Arial', 10, 'bold')
)
botao_pdf.grid(row=4, column=0, columnspan=2, pady=15)

janela.mainloop()