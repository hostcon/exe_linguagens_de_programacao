# 8. QUIZ PARANÁ
print("=== Quiz Paraná - Teste seus conhecimentos ===\n")

perguntas = [
    ("Qual a capital do Paraná?", "A", ["A) Curitiba", "B) Londrina", "C) Maringá", "D) Ponta Grossa"]),
    ("Qual é o prato típico do litoral paranaense?", "C", ["A) Feijoada", "B) Churrasco", "C) Barreado", "D) Moqueca"]),
    ("Qual time é conhecido como 'Coxa'?", "B", ["A) Athletico", "B) Coritiba", "C) Paraná Clube", "D) Operário"]),
    ("O que o paranaense mais toma no frio?", "A", ["A) Chimarrão", "B) Café", "C) Tererê", "D) Cerveja"]),
]

acertos = 0
for pergunta, resposta_certa, opcoes in perguntas:
    print(pergunta)
    for op in opcoes:
        print(op)
    resp = input("Resposta (A/B/C/D): ").upper()
    if resp == resposta_certa:
        acertos += 1
        print("Acertou!\n")
    else:
        print(f"Errou! Resposta certa: {resposta_certa}\n")

print(f"Você acertou {acertos} de {len(perguntas)} perguntas ({acertos/len(perguntas)*100:.1f}%)")