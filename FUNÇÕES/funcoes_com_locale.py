import locale

def formatar_real_locale(valor):
    # Define localização para Brasil
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    texto = locale.currency(valor, grouping=True)
    return texto


# Uso
preco = 1234.5
print(formatar_real_locale(preco))  # R$ 1.234,50