import tkinter as tk

# --- CONFIGURAÇÃO DA JANELA ---
janela = tk.Tk()
janela.title("Carrinho da Feira Simplificado")
janela.geometry("400x500")

# Variável para armazenar o total (iniciada em zero)
total_acumulado = 0.0

# --- INTERFACE: ENTRADA DE DADOS ---
# Alinhamento à esquerda (anchor='w') e preenchimento lateral (fill=tk.X)
tk.Label(janela, text="Nome do Item:", anchor='w').pack(fill=tk.X, padx=10)
entry_item = tk.Entry(janela)
entry_item.pack(fill=tk.X, padx=10, pady=5)

tk.Label(janela, text="Preço unitário:", anchor='w').pack(fill=tk.X, padx=10)
entry_preco = tk.Entry(janela)
entry_preco.pack(fill=tk.X, padx=10, pady=5)

tk.Label(janela, text="Quantidade:", anchor='w').pack(fill=tk.X, padx=10)
entry_qtd = tk.Entry(janela)
entry_qtd.pack(fill=tk.X, padx=10, pady=5)

# --- LISTA DE EXIBIÇÃO ---
# Cor de fundo cinza claro (bg) e borda suave (relief)
lista_visual = tk.Listbox(janela, height=10, bg="#f9f9f9", relief=tk.FLAT)
lista_visual.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Rótulo do Total
label_total = tk.Label(janela, text="Total: R$ 0.00", font=("Arial", 12, "bold"), fg="green")
label_total.pack(pady=5)


# --- LÓGICA DE EXECUÇÃO (Sem 'def' externa) ---
# Usamos uma função interna simples apenas para o botão funcionar
def processar_adicao():
    # Coleta os dados diretamente dos campos
    item = entry_item.get()
    # Sem try/except, o código assume que o usuário digitará números válidos
    preco = float(entry_preco.get())
    qtd = int(entry_qtd.get())

    subtotal = preco * qtd

    # Atualiza a interface
    lista_visual.insert(tk.END, f"{item} ({qtd}x) - R$ {subtotal:.2f}")

    # Atualiza o total global
    global total_acumulado
    total_acumulado += subtotal
    label_total.config(text=f"Total: R$ {total_acumulado:.2f}")


# --- BOTÕES ---
# Botão Adicionar com cor verde (bg)
btn_add = tk.Button(janela, text="Adicionar Item", command=processar_adicao, bg="#4CAF50", fg="white")
btn_add.pack(fill=tk.X, padx=10, pady=2)

# Botão Sair (Usa o comando quit da própria janela)
btn_sair = tk.Button(janela, text="Fechar", command=janela.quit, bg="#f44336", fg="white")
btn_sair.pack(fill=tk.X, padx=10, pady=10)

# Inicia o programa
janela.mainloop()