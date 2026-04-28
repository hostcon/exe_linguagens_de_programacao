def formatar_real(valor):
    # Passo 1: formatação padrão (EUA)
    texto = f"R$ {valor:,.2f}"
    # Exemplo: 1234.5 → "R$ 1,234.50"

    # Passo 2: troca vírgula por marcador temporário
    texto = texto.replace(",", "X")
    # "R$ 1X234.50"

    # Passo 3: troca ponto por vírgula (decimal BR)
    texto = texto.replace(".", ",")
    # "R$ 1X234,50"

    # Passo 4: troca marcador por ponto (milhar BR)
    texto = texto.replace("X", ".")
    # "R$ 1.234,50"

    return texto