# exercicio1_cores_ui.py
import sys
import random
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QColor

# Importa a UI gerada pelo Designer
from interface_ex1_ui import Ui_MainWindow

class ExercicioCoresUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ===== CARREGA A UI =====
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # ===== CONECTA OS SINAIS AOS SLOTS =====
        # Cada botão está conectado a uma função específica
        self.ui.btn_vermelho.clicked.connect(lambda: self.mudar_cor("#ff0000", "Vermelho"))
        self.ui.btn_verde.clicked.connect(lambda: self.mudar_cor("#00cc44", "Verde"))
        self.ui.btn_azul.clicked.connect(lambda: self.mudar_cor("#0066ff", "Azul"))
        self.ui.btn_amarelo.clicked.connect(lambda: self.mudar_cor("#ffcc00", "Amarelo"))
        self.ui.btn_roxo.clicked.connect(lambda: self.mudar_cor("#9900cc", "Roxo"))
        self.ui.btn_reset.clicked.connect(self.resetar_cor)
        self.ui.btn_aleatorio.clicked.connect(self.cor_aleatoria)
        
        # ===== CONFIGURAÇÃO INICIAL =====
        self.resetar_cor()
    
    def mudar_cor(self, cor_hex, nome_cor):
        """Muda a cor do label de amostra"""
        # Atualiza o estilo do label
        self.ui.label_amostra.setStyleSheet(
            f"background-color: {cor_hex}; border-radius: 10px; font-size: 16px; color: white;"
        )
        # Atualiza o texto
        self.ui.label_amostra.setText(f"🎨 Cor: {nome_cor}")
        # Atualiza o label de informação
        self.ui.label_info.setText(f"🟢 Cor atual: {nome_cor} ({cor_hex})")
    
    def resetar_cor(self):
        """Volta à cor padrão"""
        self.ui.label_amostra.setStyleSheet(
            "background-color: #888888; border-radius: 10px; font-size: 16px; color: white;"
        )
        self.ui.label_amostra.setText("Amostra de Cor")
        self.ui.label_info.setText("Clique nos botões para mudar a cor")
    
    def cor_aleatoria(self):
        """Gera uma cor aleatória"""
        # Gera valores RGB aleatórios
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        
        # Converte para hex
        cor_hex = f"#{r:02x}{g:02x}{b:02x}"
        nome_cor = f"RGB({r}, {g}, {b})"
        
        self.mudar_cor(cor_hex, nome_cor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = ExercicioCoresUI()
    janela.show()
    sys.exit(app.exec())