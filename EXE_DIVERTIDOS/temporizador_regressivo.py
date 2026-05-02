import time
import sys

# TEMPORIZADOR REGRESSIVO - VERSÃO MELHORADA
print("=== Temporizador do Chimarrão ===\n")

try:
    entrada = input("Quantos segundos? ")
    segundos = int(entrada)

    while segundos >= 0:
        mins, secs = divmod(segundos, 60)
        timer = f"{mins:02d}:{secs:02d}"

        # \r volta o cursor para o início da linha
        # flush=True força a exibição imediata no terminal
        print(f"\rTempo restante: {timer}", end="", flush=True)

        time.sleep(1)
        segundos -= 1

    print("\n\nTempo esgotado! Vamos que vamos! 🚀")

except ValueError:
    print("\nErro: Por favor, digite apenas números inteiros.")
except KeyboardInterrupt:
    print("\n\nTemporizador cancelado.")
