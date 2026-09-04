# exercicio3_lista_ui.py
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from interface_ex3_ui import Ui_MainWindow

class ExercicioListaUI(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ===== CARREGA A UI =====
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # ===== CONECTA OS SINAIS =====
        # Adicionar tarefa (botão e Enter)
        self.ui.btn_adicionar.clicked.connect(self.adicionar_tarefa)
        self.ui.campo_tarefa.returnPressed.connect(self.adicionar_tarefa)
        
        # Ações na lista
        self.ui.btn_concluir.clicked.connect(self.alternar_concluido)
        self.ui.btn_remover.clicked.connect(self.remover_tarefa)
        self.ui.btn_limpar.clicked.connect(self.limpar_tarefas)
        
        # Duplo clique na lista
        self.ui.lista_tarefas.itemDoubleClicked.connect(self.remover_tarefa_click)
        
        # ===== TAREFAS DE EXEMPLO =====
        exemplos = ["📚 Estudar PySide6", "💻 Praticar sinais/slots", "🎵 Criar o Horizon Player"]
        for tarefa in exemplos:
            self.ui.lista_tarefas.addItem(tarefa)
        
        self.atualizar_contador()
    
    def adicionar_tarefa(self):
        """Adiciona uma nova tarefa à lista"""
        texto = self.ui.campo_tarefa.text().strip()
        
        if texto:
            # Cria um novo item
            item = QListWidgetItem(texto)
            self.ui.lista_tarefas.addItem(item)
            
            # Limpa o campo
            self.ui.campo_tarefa.clear()
            self.atualizar_contador()
            
            # Foca no campo para a próxima digitação
            self.ui.campo_tarefa.setFocus()
    
    def alternar_concluido(self):
        """Marca/Desmarca uma tarefa como concluída"""
        linha = self.ui.lista_tarefas.currentRow()
        if linha >= 0:
            item = self.ui.lista_tarefas.item(linha)
            texto = item.text()
            
            # Verifica se já está marcada
            if texto.startswith("✅ "):
                # Desmarca
                item.setText(texto[3:])  # Remove "✅ "
                item.setForeground(Qt.GlobalColor.black)
            else:
                # Marca como concluída
                item.setText(f"✅ {texto}")
                item.setForeground(Qt.GlobalColor.gray)
    
    def remover_tarefa(self):
        """Remove a tarefa selecionada"""
        linha = self.ui.lista_tarefas.currentRow()
        if linha >= 0:
            self.ui.lista_tarefas.takeItem(linha)
            self.atualizar_contador()
    
    def remover_tarefa_click(self, item):
        """Remove a tarefa quando recebe duplo clique"""
        linha = self.ui.lista_tarefas.row(item)
        self.ui.lista_tarefas.takeItem(linha)
        self.atualizar_