import tkinter as tk
import random




class CaçaNiquel:
    def __init__(self):
        self.saldo = 20.0
        self.custo_giro = 2.0
        
        self.simbolos = ["🍵", "🌰", "🐂", "⭐", "🍊", "🍒", "🛎️"]
        self.premios = {3: 20, 2: 5}  # 3 iguais = 20, 2 iguais = 5
        
        self.root = tk.Tk()
        self.root.title("🎰 Kasinão do Sesi")
        self.root.geometry("420x380")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.criar_interface()
        
    def criar_interface(self):
        # Título
        titulo = tk.Label(self.root, text="🎰 Kasinão do Sesi", 
                         font=("Arial", 20, "bold"), fg="#ffd700", bg="#1e1e1e")
        titulo.pack(pady=15)

        # Frame dos slots
        self.frame_slots = tk.Frame(self.root, bg="#1e1e1e")
        self.frame_slots.pack(pady=20)

        self.slot1 = tk.Label(self.frame_slots, text="❓", font=("Arial", 48), width=3, bg="#2a2a2a", relief="solid")
        self.slot2 = tk.Label(self.frame_slots, text="❓", font=("Arial", 48), width=3, bg="#2a2a2a", relief="solid")
        self.slot3 = tk.Label(self.frame_slots, text="❓", font=("Arial", 48), width=3, bg="#2a2a2a", relief="solid")

        self.slot1.pack(side="left", padx=8)
        self.slot2.pack(side="left", padx=8)
        self.slot3.pack(side="left", padx=8)

        # Resultado
        self.resultado_label = tk.Label(self.root, text="Clique em GIRAR para começar!", 
                                      font=("Arial", 14), fg="white", bg="#1e1e1e")
        self.resultado_label.pack(pady=15)

        # Saldo
        self.saldo_label = tk.Label(self.root, text=f"Saldo: R$ {self.saldo:.2f}", 
                                  font=("Arial", 16, "bold"), fg="#00ff00", bg="#1e1e1e")
        self.saldo_label.pack(pady=10)

        # Botão Girar
        self.botao = tk.Button(self.root, text="🎰 GIRAR (R$ 2,00)", font=("Arial", 14, "bold"),
                             bg="#ff4444", fg="white", height=2, width=20, command=self.girar)
        self.botao.pack(pady=20)

    def girar(self):
        if self.saldo < self.custo_giro:
            self.resultado_label.config(text="💸 Saldo insuficiente!", fg="red")
            return

        self.saldo -= self.custo_giro
        
        # Gira os símbolos
        resultado = [random.choice(self.simbolos) for _ in range(3)]
        
        self.slot1.config(text=resultado[0])
        self.slot2.config(text=resultado[1])
        self.slot3.config(text=resultado[2])

        # Verifica vitória
        if resultado[0] == resultado[1] == resultado[2]:
            premio = 20
            self.saldo += premio
            self.resultado_label.config(text=f"🎉 JACKPOT!!! +R$ {premio}", fg="#00ff00")
            
        elif len(set(resultado)) == 2:  # Dois símbolos iguais
            premio = 5
            self.saldo += premio
            self.resultado_label.config(text=f"👍 Boa! +R$ {premio}", fg="#00cc00")
            
        else:
            self.resultado_label.config(text="😢 Tente novamente...", fg="#aaaaaa")

        self.saldo_label.config(text=f"Saldo: R$ {self.saldo:.2f}")

    def iniciar(self):
        self.root.mainloop()


# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    jogo = CaçaNiquel()
    jogo.iniciar()
