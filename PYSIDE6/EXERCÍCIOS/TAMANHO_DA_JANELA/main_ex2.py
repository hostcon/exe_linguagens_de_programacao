# exercicio2_tamanho_ui.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt

from interface_ex2_ui import Ui_MainWindow

class ExercicioTamanhoUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ===== CARREGA A UI =====
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # ===== GUARDA O TAMANHO ORIGINAL =====
        self.largura_original = 500
        self.altura_original = 400
        self.proporcao = self.largura_original / self.altura_original
        
        # ===== CONECTA OS SINAIS =====
        # Sliders
        self.ui.slider_largura.valueChanged.connect(self.atualizar_largura)
        self.ui.slider_altura.valueChanged.connect(self.atualizar_altura)
        
        # Checkbox - Manter Proporção
        self.ui.checkbox_proporcao.stateChanged.connect(self.alternar_proporcao)
        
        # Botões de tamanhos pré-definidos
        self.ui.btn_pequeno.clicked.connect(lambda: self.definir_tamanho(400, 300))
        self.ui.btn_medio.clicked.connect(lambda: self.definir_tamanho(600, 450))
        self.ui.btn_grande.clicked.connect(lambda: self.definir_tamanho(800, 600))
        self.ui.btn_maximo.clicked.connect(self.maximizar)
        self.ui.btn_reset.clicked.connect(self.resetar)
    
    def atualizar_largura(self, valor):
        """Atualiza a largura da janela"""
        self.ui.label_largura_valor.setText(str(valor))
        
        # Se mantiver proporção, ajusta a altura
        if self.ui.checkbox_proporcao.isChecked():
            nova_altura = int(valor / self.proporcao)
            self.ui.slider_altura.setValue(nova_altura)
        
        self.resize(valor, self.ui.slider_altura.value())
        self.atualizar_info()
    
    def atualizar_altura(self, valor):
        """Atualiza a altura da janela"""
        self.ui.label_altura_valor.setText(str(valor))
        
        # Se mantiver proporção, ajusta a largura
        if self.ui.checkbox_proporcao.isChecked():
            nova_largura = int(valor * self.proporcao)
            self.ui.slider_largura.setValue(nova_largura)
        
        self.resize(self.ui.slider_largura.value(), valor)
        self.atualizar_info()
    
    def alternar_proporcao(self, estado):
        """Ativa/desativa a manutenção de proporção"""
        if estado == Qt.Checked:
            self.ui.label_info.setText("🔒 Proporção mantida!")
            self.proporcao = self.ui.slider_largura.value() / self.ui.slider_altura.value()
        else:
            self.ui.label_info.setText("🔓 Proporção livre")
    
    def definir_tamanho(self, largura, altura):
        """Define um tamanho específico"""
        self.ui.slider_largura.setValue(largura)
        self.ui.slider_altura.setValue(altura)
    
    def maximizar(self):
        """Maximiza a janela"""
        self.showMaximized()
        self.ui.label_info.setText("📌 Janela maximizada!")
    
    def resetar(self):
        """Reseta para o tamanho original"""
        self.ui.slider_largura.setValue(self.largura_original)
        self.ui.slider_altura.setValue(self.altura_original)
        self.showNormal()
        self.ui.label_info.setText("🔄 Tamanho resetado!")
    
    def atualizar_info(self):
        """Atualiza o label de informações"""
        larg = self.ui.slider_largura.value()
        alt = self.ui.slider_altura.value()
        self.ui.label_info.setText(f"Dimensões: {larg} x {alt}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = ExercicioTamanhoUI()
    janela.show()
    sys.exit(app.exec())