import tkinter as tk
import locale

# ==================================================
# CONFIGURAÇÃO DE LOCALIZAÇÃO (Brasil UTF-8)
# ==================================================

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    # Windows geralmente usa outro nome
    locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')

# ==================================================
# CONFIGURAÇÃO DA JANELA
# ==================================================

janela = tk.Tk()
janela.title("Carrinho da Feira Simplificado")
janela.geometry("400x500")

# Variável do total
total_acumulado = 0.0

# ==================================================
# CAMPOS
# ==================================================

tk.Label(janela, text="Nome do Item:", anchor='w').pack(fill=tk.X, padx=10)

entry_item = tk.Entry(janela)
entry_item.pack(fill=tk.X, padx=10, pady=5)

tk.Label(janela, text="Preço unitário:", anchor='w').pack(fill=tk.X, padx=10)

entry_preco = tk.Entry(janela)
entry_preco.pack(fill=tk.X, padx=10, pady=5)

tk.Label(janela, text="Quantidade:", anchor='w').pack(fill=tk.X, padx=10)

entry_qtd = tk.Entry(janela)
entry_qtd.pack(fill=tk.X, padx=10, pady=5)

# ==================================================
# LISTA VISUAL
# ==================================================

lista_visual = tk.Listbox(
    janela,
    height=10,
    bg="#f9f9f9",
    relief=tk.FLAT,
    font=("Arial", 10)
)

lista_visual.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# ==================================================
# TOTAL
# ==================================================

label_total = tk.Label(
    janela,
    text="Total: R$ 0,00",
    font=("Arial", 12, "bold"),
    fg="green"
)

label_total.pack(pady=5)

# ==================================================
# FUNÇÃO PRINCIPAL
# ==================================================

def processar_adicao():

    global total_acumulado

    item = entry_item.get()

    # Aceita vírgula brasileira
    preco_texto = entry_preco.get().replace(',', '.')
    preco = float(preco_texto)

    qtd = int(entry_qtd.get())

    subtotal = preco * qtd

    total_acumulado += subtotal

    # Formatação monetária brasileira
    subtotal_formatado = locale.currency(subtotal, grouping=True)
    total_formatado = locale.currency(total_acumulado, grouping=True)

    # Adiciona na lista
    lista_visual.insert(
        tk.END,
        f"{item} ({qtd}x) - {subtotal_formatado}"
    )

    # Atualiza total
    label_total.config(text=f"Total: {total_formatado}")

    # Limpa os campos
    entry_item.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_qtd.delete(0, tk.END)

    # Retorna foco
    entry_item.focus_set()

# ==================================================
# BOTÕES
# ==================================================

btn_add = tk.Button(
    janela,
    text="Adicionar Item",
    command=processar_adicao,
    bg="#4CAF50",
    fg="white"
)

btn_add.pack(fill=tk.X, padx=10, pady=2)

btn_sair = tk.Button(
    janela,
    text="Fechar",
    command=janela.quit,
    bg="#f44336",
    fg="white"
)

btn_sair.pack(fill=tk.X, padx=10, pady=10)

# ==================================================
# EXECUÇÃO
# ==================================================

janela.mainloop()