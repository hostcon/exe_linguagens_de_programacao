import time
import os
import platform
import sys


def shutdown():
    sistema = platform.system().lower()
    try:
        if "windows" in sistema:
            os.system("shutdown /s /t 0")
        elif "linux" in sistema:
            os.system("sudo shutdown now")
        elif "darwin" in sistema:  # macOS
            os.system("sudo shutdown -h now")
        else:
            print("\nSistema operacional não suportado.")
    except Exception as e:
        print(f"\nErro ao desligar: {e}")


def temporizador_com_shutdown():
    print("=== Temporizador Trolator Tabajara ===\n")

    try:
        entrada = input("Quantos segundos até o desligamento? ")
        segundos = int(entrada)

        if segundos <= 0:
            print("Por favor, digite um número positivo!")
            return

        print(f"\nO computador será desligado em {segundos} segundos...\n")

        while segundos > 0:
            # divmod() divide o tempo e retorna minutos e segundos
            # Exemplo: divmod(125, 60) → retorna (2, 5) → 2 minutos e 5 segundos
            mins, secs = divmod(segundos, 60)
            
            # Formata para sempre mostrar 2 dígitos (ex: 05:03)
            timer = f"{mins:02d}:{secs:02d}"

            # Bip sonoro apenas nos últimos 10 segundos
            bip = "\a" if 0 < segundos <= 10 else ""

            # ==================== EXPLICAÇÃO DOS CARACTERES ESPECIAIS ====================
            # \r  → Carriage Return (Retorno do Carro)
            #     Faz o cursor voltar para o INÍCIO da linha atual.
            #     Isso permite sobrescrever o texto anterior, criando o efeito de contador regressivo na mesma linha.

            # end="" → Impede o print() de pular para a próxima linha (não adiciona \n)

            # flush=True → Força o Python a imprimir imediatamente o que está no buffer.
            #     Sem isso, o texto pode não aparecer em tempo real quando usamos \r.
            # =============================================================================
            print(f"\rTempo restante: {timer}{bip}", end="", flush=True)

            time.sleep(1)
            segundos -= 1

        # Quando o loop termina (segundos == 0)
        print("\n\nIniciando desligamento... Tchau! 👋")
        shutdown()

    except ValueError:
        print("\nErro: Por favor, digite apenas números inteiros.")
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário. 😌")


if __name__ == "__main__":
    temporizador_com_shutdown()
