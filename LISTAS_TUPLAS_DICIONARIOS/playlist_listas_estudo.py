# Inicializando a playlist vazia antes do laço para não apagar os dados
playlist = []

while True:
    # Exibição do Menu de Opções
    print("\n" + "="*30)
    print("      MENU DA PLAYLIST")
    print("="*30)
    print("1. Adicionar música")
    print("2. Ver playlist atual")
    print("3. Alterar música por posição")
    print("4. Remover música por nome")
    print("5. Sair do programa")
    print("="*30)
    
    # Entrada da opção do usuário
    opcao = input("Escolha uma opção (1-5): ")
    print("-" * 30)

    # --- OPÇÃO 1: ADICIONAR ---
    if opcao == "1":
        nova_musica = input("Digite o nome da música para adicionar: ")
        playlist.append(nova_musica)
        print(f"'{nova_musica}' foi adicionada com sucesso!")

    # --- OPÇÃO 2: EXIBIR ---
    elif opcao == "2":
        if len(playlist) == 0:
            print("Sua playlist está vazia no momento!")
        else:
            print("--- SUA PLAYLIST ---")
            # O enumerate ajuda a mostrar o índice para o usuário saber como alterar depois
            for indice, musica in enumerate(playlist):
                print(f"Posição {indice} -> {musica}")

    # --- OPÇÃO 3: ALTERAR ---
    elif opcao == "3":
        if len(playlist) == 0:
            print("Não há músicas para alterar. A playlist está vazia!")
        else:
            posicao = int(input("Digite o número da posição que deseja alterar: "))
            
            # Validação para garantir que o índice existe na lista
            if 0 <= posicao < len(playlist):
                musica_antiga = playlist[posicao]
                nova_musica = input(f"Substituir '{musica_antiga}' por: ")
                playlist[posicao] = nova_musica
                print("Música alterada com sucesso!")
            else:
                print("Posição inválida! Verifique os números na opção 2.")

    # --- OPÇÃO 4: REMOVER ---
    elif opcao == "4":
        if len(playlist) == 0:
            print("Não há músicas para remover. A playlist está vazia!")
        else:
            musica_remover = input("Digite o nome exato da música que deseja remover: ")
            
            # Verificamos se o elemento está na lista antes de tentar remover (evita erro)
            if musica_remover in playlist:
                playlist.remove(musica_remover)
                print(f"'{musica_remover}' removida com sucesso!")
            else:
                print("Música não encontrada. Atenção com maiúsculas e minúsculas!")

    # --- OPÇÃO 5: SAIR ---
    elif opcao == "5":
        print("Encerrando o sistema de música. Até logo!")
        break  # Interrompe o laço 'while True' e finaliza o programa

    # --- TRATAMENTO DE OPÇÃO INVÁLIDA ---
    else:
        print("Opção inválida! Escolha um número de 1 a 5.")
