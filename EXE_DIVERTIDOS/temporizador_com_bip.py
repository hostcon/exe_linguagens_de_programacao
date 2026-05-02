import time
import sys

# TEMPORIZADOR DO CHIMARRÃO - VERSÃO COM BIP
print("=== Temporizador do Chimarrão (Versão com Bip) ===\n")

try:
    entrada = input("Quantos segundos? ")
    segundos = int(entrada)

    while segundos >= 0:
        mins, secs = divmod(segundos, 60)
        timer = f"{mins:02d}:{secs:02d}"

        # Lógica do Bip: ativa nos 10 segundos finais
        # \a é o caractere especial que faz o computador apitar
        bip = ""
        if 0 < segundos <= 10:
            bip = "\a"

            # Exibe o tempo e "imprime" o bip (o bip não aparece, apenas soa)
        print(f"\rTempo restante: {timer}{bip}", end="", flush=True)

        time.sleep(1)
        segundos -= 1

    # Três bips finais para o alerta definitivo
    print("\a\a\a")
    print("\n\nTempo esgotado! Vamos que vamos! 🚀")

except ValueError:
    print("\nErro: Por favor, digite apenas números inteiros.")
except KeyboardInterrupt:
    print("\n\nTemporizador cancelado.")
