import time
import sys
import os
import platform


def desligar_computador():
    """Executa o comando de desligamento baseado no sistema operacional."""
    sistema = platform.system().lower()

    try:
        if "windows" in sistema:
            # /s = shutdown, /t 0 = tempo zero (imediato)
            os.system("shutdown /s /t 0")
        elif "linux" in sistema or "darwin" in sistema:  # darwin é macOS
            # now = imediato. Pode exigir sudo em alguns Linux
            os.system("shutdown now")
        else:
            print("\nSistema operacional não reconhecido para desligamento automático.")
    except Exception as e:
        print(f"\nErro ao tentar desligar: {e}")


def temporizador_com_shutdown():
    print("=== Temporizador com Desligamento Automático ===\n")
    print("AVISO: Este script desligará seu computador ao final da contagem!")

    try:
        entrada = input("Quantos segundos até o desligamento? ")
        segundos = int(entrada)

        while segundos >= 0:
            mins, secs = divmod(segundos, 60)
            timer = f"{mins:02d}:{secs:02d}"

            # Bip nos 10 segundos finais
            bip = "\a" if 0 < segundos <= 10 else ""

            print(f"\rTempo restante: {timer}{bip}", end="", flush=True)

            time.sleep(1)
            segundos -= 1

        print("\n\nIniciando desligamento... Tchau! 👋")
        time.sleep(2)  # Pequena pausa para o usuário ler a mensagem

        # Chama a função de desligamento
        desligar_computador()

    except ValueError:
        print("\nErro: Por favor, digite apenas números inteiros.")
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")


if __name__ == "__main__":
    temporizador_com_shutdown()