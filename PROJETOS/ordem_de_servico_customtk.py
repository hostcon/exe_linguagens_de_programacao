import customtkinter as ctk
from tkinter import messagebox
from fpdf import FPDF

# ==================================
# Configurações de Tema (Opcional)
# ==================================
ctk.set_appearance_mode("dark")      # "system", "light", "dark"
ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"

# ==================================
# Função: Gerar PDF
# ==================================
def gerar_pdf():
    # ========== OBTENDO DADOS DA INTERFACE ==========
    cliente = entrada_cliente.get()
    servico = combo_servico.get()
    valor = entrada_valor.get()

    # ========== VALIDAÇÃO DOS CAMPOS ==========
    if not cliente or not servico or not valor:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")
        return

    try:
        # ========== CRIAÇÃO DO OBJETO PDF ==========
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # ========== TÍTULO ==========
        pdf.cell(200, 10, txt="ORDEM DE SERVIÇO", ln=1, align="C")
        pdf.ln(10)

        # ========== DADOS ==========
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=1)
        pdf.cell(200, 10, txt=f"Servico: {servico}", ln=1)
        pdf.cell(200, 10, txt=f"Valor: R$ {valor}", ln=1)

        # ========== SALVA O ARQUIVO PDF ==========
        pdf.output("ordem_de_servico.pdf")

        messagebox.showinfo("Sucesso", "PDF gerado com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar PDF: {e}")

# ==================================
# Janela Principal
# ==================================
janela = ctk.CTk()
janela.title("Gerador de Ordem de Serviço")
janela.geometry("400x260")  # Ajustei um pouco para o visual do CTk

# ==================================
# CAMPO: CLIENTE
# ==================================
lbl_cliente = ctk.CTkLabel(janela, text="Cliente:")
lbl_cliente.grid(row=0, column=0, sticky="w", padx=10, pady=8)

entrada_cliente = ctk.CTkEntry(janela, width=220)
entrada_cliente.grid(row=0, column=1, padx=10, pady=8)

# ==================================
# CAMPO: SERVIÇO (CTkComboBox)
# ==================================
lbl_servico = ctk.CTkLabel(janela, text="Serviço:")
lbl_servico.grid(row=1, column=0, sticky="w", padx=10, pady=8)

servicos = [
    "Formatação de Computador",
    "Instalação de Windows",
    "Manutenção de Rede",
    "Criação de Site",
    "Suporte Técnico"
]

# No CustomTkinter, o combobox equivalente é o CTkComboBox.
# Ele já vem com uma setinha para abrir as opções.
# Para impedir digitação livre, usamos state="readonly".
combo_servico = ctk.CTkComboBox(
    janela,
    values=servicos,
    width=220,
    state="readonly"   # impede o usuário de digitar valores fora da lista
)
combo_servico.grid(row=1, column=1, padx=10, pady=8)

# Define o primeiro item como selecionado por padrão
combo_servico.set(servicos[0])

# ==================================
# CAMPO: VALOR
# ==================================
lbl_valor = ctk.CTkLabel(janela, text="Valor (R$):")
lbl_valor.grid(row=2, column=0, sticky="w", padx=10, pady=8)

entrada_valor = ctk.CTkEntry(janela, width=220)
entrada_valor.grid(row=2, column=1, padx=10, pady=8)

# ==================================
# BOTÃO: GERAR PDF
# ==================================
# No CTk não usamos bg/fg, e sim fg_color e text_color.
botao_pdf = ctk.CTkButton(
    janela,
    text="Gerar PDF",
    command=gerar_pdf,
    fg_color="green",       # fundo verde
    hover_color="#0a7a0a",  # tom mais escuro ao passar o mouse (opcional)
    text_color="white",     # texto branco
    width=160
)
botao_pdf.grid(row=3, column=0, columnspan=2, pady=20)

# ==================================
# Loop Principal
# ==================================
janela.mainloop()
