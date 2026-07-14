"""
Sistema PDV (Ponto de Venda) - Interface gráfica com PySide6
Banco de dados: SQLite (arquivo pdv.db, criado automaticamente)

Estrutura:
  - Aba "PDV (Venda)": busca de produto, carrinho, fechamento da venda
  - Aba "Produtos": cadastro/edição/exclusão de produtos (CRUD)
  - Aba "Histórico": lista de vendas realizadas e detalhe dos itens

Para rodar:
    pip install PySide6
    python main.py
"""

import sys

from PySide6.QtCore import Qt, QDate
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QDoubleSpinBox, QSpinBox, QMessageBox, QHeaderView,
    QGroupBox, QFormLayout, QDateEdit, QDialog, QAbstractItemView
)

from database import Database


MOEDA = "R$"


def fmt_moeda(valor):
    """Formata um número float no padrão monetário brasileiro (R$ 1.234,56)."""
    return f"{MOEDA} {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ---------------------------------------------------------------------------
# ABA DE VENDA (PDV)
# ---------------------------------------------------------------------------
class TabVenda(QWidget):
    def __init__(self, db: Database, atualizar_callback=None):
        super().__init__()
        self.db = db
        self.atualizar_callback = atualizar_callback
        self.carrinho = []  # lista de dicts: produto_id, nome_produto, quantidade, preco_unitario, subtotal
        self._montar_ui()

    def _montar_ui(self):
        layout_principal = QHBoxLayout(self)

        # ---------- Coluna esquerda: busca de produto ----------
        col_esquerda = QVBoxLayout()

        titulo_busca = QLabel("Buscar Produto")
        titulo_busca.setStyleSheet("font-size: 16px; font-weight: bold; color: #1a5276;")
        col_esquerda.addWidget(titulo_busca)

        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Código de barras ou nome... (Enter para buscar/adicionar)")
        self.campo_busca.returnPressed.connect(self._buscar_produto)
        col_esquerda.addWidget(self.campo_busca)

        self.tabela_busca = QTableWidget(0, 4)
        self.tabela_busca.setHorizontalHeaderLabels(["Nome", "Preço", "Estoque", "Categoria"])
        self.tabela_busca.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_busca.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela_busca.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela_busca.doubleClicked.connect(self._adicionar_ao_carrinho)
        col_esquerda.addWidget(self.tabela_busca)

        linha_qtd = QHBoxLayout()
        linha_qtd.addWidget(QLabel("Quantidade:"))
        self.spin_qtd = QSpinBox()
        self.spin_qtd.setRange(1, 9999)
        self.spin_qtd.setValue(1)
        linha_qtd.addWidget(self.spin_qtd)

        btn_adicionar = QPushButton("Adicionar ao carrinho ▶")
        btn_adicionar.setStyleSheet("background-color: #2874a6; color: white; padding: 6px; font-weight: bold;")
        btn_adicionar.clicked.connect(self._adicionar_ao_carrinho)
        linha_qtd.addWidget(btn_adicionar)
        col_esquerda.addLayout(linha_qtd)

        layout_principal.addLayout(col_esquerda, 55)

        # ---------- Coluna direita: carrinho / fechamento ----------
        col_direita = QVBoxLayout()

        titulo_carrinho = QLabel("Carrinho de Venda")
        titulo_carrinho.setStyleSheet("font-size: 16px; font-weight: bold; color: #1a5276;")
        col_direita.addWidget(titulo_carrinho)

        self.tabela_carrinho = QTableWidget(0, 4)
        self.tabela_carrinho.setHorizontalHeaderLabels(["Produto", "Qtd", "Preço Unit.", "Subtotal"])
        self.tabela_carrinho.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela_carrinho.setEditTriggers(QAbstractItemView.NoEditTriggers)
        col_direita.addWidget(self.tabela_carrinho)

        btn_remover = QPushButton("Remover item selecionado")
        btn_remover.clicked.connect(self._remover_item)
        col_direita.addWidget(btn_remover)

        self.label_total = QLabel(f"TOTAL: {fmt_moeda(0)}")
        self.label_total.setStyleSheet("font-size: 22px; font-weight: bold; color: #145a32;")
        col_direita.addWidget(self.label_total)

        linha_pagamento = QHBoxLayout()
        linha_pagamento.addWidget(QLabel("Forma de pagamento:"))
        self.combo_pagamento = QComboBox()
        self.combo_pagamento.addItems(["Dinheiro", "Cartão de Débito", "Cartão de Crédito", "Pix"])
        linha_pagamento.addWidget(self.combo_pagamento)
        col_direita.addLayout(linha_pagamento)

        linha_botoes = QHBoxLayout()
        btn_finalizar = QPushButton("FINALIZAR VENDA ✔")
        btn_finalizar.setStyleSheet(
            "background-color: #1e8449; color: white; padding: 10px; font-weight: bold; font-size: 14px;")
        btn_finalizar.clicked.connect(self._finalizar_venda)
        btn_cancelar = QPushButton("Cancelar / Limpar")
        btn_cancelar.setStyleSheet("background-color: #c0392b; color: white; padding: 10px; font-weight: bold;")
        btn_cancelar.clicked.connect(self._limpar_carrinho)
        linha_botoes.addWidget(btn_finalizar)
        linha_botoes.addWidget(btn_cancelar)
        col_direita.addLayout(linha_botoes)

        layout_principal.addLayout(col_direita, 45)

        self._buscar_produto()  # carrega lista inicial de produtos

    # ---------------- lógica ----------------
    def _buscar_produto(self):
        filtro = self.campo_busca.text().strip()

        # se bateu exatamente um código de barras cadastrado, adiciona direto
        # (comportamento de leitor de código de barras)
        if filtro:
            produto = self.db.buscar_produto_por_codigo(filtro)
            if produto:
                self._adicionar_produto(produto, self.spin_qtd.value())
                self.campo_busca.clear()
                return

        produtos = self.db.listar_produtos(filtro)
        self.tabela_busca.setRowCount(0)
        for p in produtos:
            row = self.tabela_busca.rowCount()
            self.tabela_busca.insertRow(row)
            self.tabela_busca.setItem(row, 0, QTableWidgetItem(p["nome"]))
            self.tabela_busca.setItem(row, 1, QTableWidgetItem(fmt_moeda(p["preco"])))
            self.tabela_busca.setItem(row, 2, QTableWidgetItem(str(p["estoque"])))
            self.tabela_busca.setItem(row, 3, QTableWidgetItem(p["categoria"] or ""))
            self.tabela_busca.item(row, 0).setData(Qt.UserRole, p["id"])

    def _adicionar_ao_carrinho(self):
        row = self.tabela_busca.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Atenção", "Selecione um produto na lista de busca.")
            return
        produto_id = self.tabela_busca.item(row, 0).data(Qt.UserRole)
        produto = self.db.buscar_produto_por_id(produto_id)
        if produto:
            self._adicionar_produto(produto, self.spin_qtd.value())

    def _adicionar_produto(self, produto, quantidade):
        if produto["estoque"] < quantidade:
            QMessageBox.warning(
                self, "Estoque insuficiente",
                f"Estoque disponível para '{produto['nome']}': {produto['estoque']}"
            )
            return

        # se o produto já está no carrinho, apenas soma a quantidade
        for item in self.carrinho:
            if item["produto_id"] == produto["id"]:
                item["quantidade"] += quantidade
                item["subtotal"] = item["quantidade"] * item["preco_unitario"]
                self._atualizar_tabela_carrinho()
                return

        self.carrinho.append({
            "produto_id": produto["id"],
            "nome_produto": produto["nome"],
            "quantidade": quantidade,
            "preco_unitario": produto["preco"],
            "subtotal": produto["preco"] * quantidade
        })
        self._atualizar_tabela_carrinho()

    def _remover_item(self):
        row = self.tabela_carrinho.currentRow()
        if row >= 0:
            del self.carrinho[row]
            self._atualizar_tabela_carrinho()

    def _atualizar_tabela_carrinho(self):
        self.tabela_carrinho.setRowCount(0)
        total = 0
        for item in self.carrinho:
            row = self.tabela_carrinho.rowCount()
            self.tabela_carrinho.insertRow(row)
            self.tabela_carrinho.setItem(row, 0, QTableWidgetItem(item["nome_produto"]))
            self.tabela_carrinho.setItem(row, 1, QTableWidgetItem(str(item["quantidade"])))
            self.tabela_carrinho.setItem(row, 2, QTableWidgetItem(fmt_moeda(item["preco_unitario"])))
            self.tabela_carrinho.setItem(row, 3, QTableWidgetItem(fmt_moeda(item["subtotal"])))
            total += item["subtotal"]
        self.label_total.setText(f"TOTAL: {fmt_moeda(total)}")

    def _limpar_carrinho(self):
        self.carrinho = []
        self._atualizar_tabela_carrinho()

    def _finalizar_venda(self):
        if not self.carrinho:
            QMessageBox.warning(self, "Atenção", "O carrinho está vazio.")
            return

        total = sum(item["subtotal"] for item in self.carrinho)
        forma_pagamento = self.combo_pagamento.currentText()

        confirmacao = QMessageBox.question(
            self, "Confirmar venda",
            f"Finalizar venda no valor de {fmt_moeda(total)} via {forma_pagamento}?"
        )
        if confirmacao != QMessageBox.Yes:
            return

        venda_id = self.db.registrar_venda(total, forma_pagamento, self.carrinho)
        QMessageBox.information(
            self, "Venda concluída",
            f"Venda #{venda_id} registrada com sucesso!\nTotal: {fmt_moeda(total)}"
        )
        self._limpar_carrinho()
        self._buscar_produto()  # atualiza estoque exibido na lista de busca

        if self.atualizar_callback:
            self.atualizar_callback()


# ---------------------------------------------------------------------------
# ABA DE PRODUTOS (CADASTRO / CRUD)
# ---------------------------------------------------------------------------
class TabProdutos(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.produto_selecionado_id = None
        self._montar_ui()
        self._carregar_produtos()

    def _montar_ui(self):
        layout = QHBoxLayout(self)

        # ---------- formulário à esquerda ----------
        form_box = QGroupBox("Cadastro de Produto")
        form_layout = QFormLayout()

        self.input_nome = QLineEdit()
        self.input_codigo = QLineEdit()
        self.input_categoria = QLineEdit()
        self.input_preco = QDoubleSpinBox()
        self.input_preco.setRange(0, 999999)
        self.input_preco.setDecimals(2)
        self.input_preco.setPrefix("R$ ")
        self.input_estoque = QSpinBox()
        self.input_estoque.setRange(0, 999999)

        form_layout.addRow("Nome:", self.input_nome)
        form_layout.addRow("Código de barras:", self.input_codigo)
        form_layout.addRow("Categoria:", self.input_categoria)
        form_layout.addRow("Preço:", self.input_preco)
        form_layout.addRow("Estoque:", self.input_estoque)

        botoes = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.setStyleSheet("background-color: #1e8449; color: white; padding: 6px; font-weight: bold;")
        btn_salvar.clicked.connect(self._salvar_produto)
        btn_novo = QPushButton("Novo")
        btn_novo.clicked.connect(self._limpar_formulario)
        btn_excluir = QPushButton("Excluir")
        btn_excluir.setStyleSheet("background-color: #c0392b; color: white; padding: 6px; font-weight: bold;")
        btn_excluir.clicked.connect(self._excluir_produto)
        botoes.addWidget(btn_salvar)
        botoes.addWidget(btn_novo)
        botoes.addWidget(btn_excluir)

        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.addLayout(botoes)
        form_container.addStretch()
        form_box.setLayout(form_container)

        layout.addWidget(form_box, 35)

        # ---------- tabela à direita ----------
        col_direita = QVBoxLayout()
        self.campo_busca = QLineEdit()
        self.campo_busca.setPlaceholderText("Buscar produto por nome ou código...")
        self.campo_busca.textChanged.connect(self._carregar_produtos)
        col_direita.addWidget(self.campo_busca)

        self.tabela = QTableWidget(0, 5)
        self.tabela.setHorizontalHeaderLabels(["Nome", "Código", "Categoria", "Preço", "Estoque"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabela.doubleClicked.connect(self._carregar_no_formulario)
        col_direita.addWidget(self.tabela)

        layout.addLayout(col_direita, 65)

    def _carregar_produtos(self):
        filtro = self.campo_busca.text().strip()
        produtos = self.db.listar_produtos(filtro)
        self.tabela.setRowCount(0)
        for p in produtos:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            self.tabela.setItem(row, 0, QTableWidgetItem(p["nome"]))
            self.tabela.setItem(row, 1, QTableWidgetItem(p["codigo_barras"] or ""))
            self.tabela.setItem(row, 2, QTableWidgetItem(p["categoria"] or ""))
            self.tabela.setItem(row, 3, QTableWidgetItem(fmt_moeda(p["preco"])))
            self.tabela.setItem(row, 4, QTableWidgetItem(str(p["estoque"])))
            self.tabela.item(row, 0).setData(Qt.UserRole, p["id"])

    def _carregar_no_formulario(self):
        row = self.tabela.currentRow()
        if row < 0:
            return
        produto_id = self.tabela.item(row, 0).data(Qt.UserRole)
        produto = self.db.buscar_produto_por_id(produto_id)
        if produto:
            self.produto_selecionado_id = produto["id"]
            self.input_nome.setText(produto["nome"])
            self.input_codigo.setText(produto["codigo_barras"] or "")
            self.input_categoria.setText(produto["categoria"] or "")
            self.input_preco.setValue(produto["preco"])
            self.input_estoque.setValue(produto["estoque"])

    def _limpar_formulario(self):
        self.produto_selecionado_id = None
        self.input_nome.clear()
        self.input_codigo.clear()
        self.input_categoria.clear()
        self.input_preco.setValue(0)
        self.input_estoque.setValue(0)

    def _salvar_produto(self):
        nome = self.input_nome.text().strip()
        if not nome:
            QMessageBox.warning(self, "Atenção", "Informe o nome do produto.")
            return

        codigo = self.input_codigo.text().strip()
        categoria = self.input_categoria.text().strip()
        preco = self.input_preco.value()
        estoque = self.input_estoque.value()

        try:
            if self.produto_selecionado_id:
                self.db.atualizar_produto(self.produto_selecionado_id, nome, codigo, categoria, preco, estoque)
                QMessageBox.information(self, "Sucesso", "Produto atualizado com sucesso!")
            else:
                self.db.inserir_produto(nome, codigo, categoria, preco, estoque)
                QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso!")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Não foi possível salvar o produto.\n{e}")
            return

        self._limpar_formulario()
        self._carregar_produtos()

    def _excluir_produto(self):
        if not self.produto_selecionado_id:
            QMessageBox.warning(self, "Atenção", "Selecione um produto para excluir.")
            return
        confirmacao = QMessageBox.question(
            self, "Confirmar exclusão", "Tem certeza que deseja excluir este produto?"
        )
        if confirmacao == QMessageBox.Yes:
            self.db.excluir_produto(self.produto_selecionado_id)
            self._limpar_formulario()
            self._carregar_produtos()


# ---------------------------------------------------------------------------
# ABA DE HISTÓRICO DE VENDAS
# ---------------------------------------------------------------------------
class DialogItensVenda(QDialog):
    """Janela de detalhe mostrando os itens de uma venda específica."""

    def __init__(self, db: Database, venda_id, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Itens da Venda #{venda_id}")
        self.resize(500, 300)
        layout = QVBoxLayout(self)

        tabela = QTableWidget(0, 4)
        tabela.setHorizontalHeaderLabels(["Produto", "Qtd", "Preço Unit.", "Subtotal"])
        tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(tabela)

        itens = db.itens_da_venda(venda_id)
        for item in itens:
            row = tabela.rowCount()
            tabela.insertRow(row)
            tabela.setItem(row, 0, QTableWidgetItem(item["nome_produto"]))
            tabela.setItem(row, 1, QTableWidgetItem(str(item["quantidade"])))
            tabela.setItem(row, 2, QTableWidgetItem(fmt_moeda(item["preco_unitario"])))
            tabela.setItem(row, 3, QTableWidgetItem(fmt_moeda(item["subtotal"])))


class TabHistorico(QWidget):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self._montar_ui()
        self.atualizar()

    def _montar_ui(self):
        layout = QVBoxLayout(self)

        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("De:"))
        self.data_inicio = QDateEdit(calendarPopup=True)
        self.data_inicio.setDate(QDate.currentDate().addDays(-30))
        filtro_layout.addWidget(self.data_inicio)

        filtro_layout.addWidget(QLabel("Até:"))
        self.data_fim = QDateEdit(calendarPopup=True)
        self.data_fim.setDate(QDate.currentDate())
        filtro_layout.addWidget(self.data_fim)

        btn_filtrar = QPushButton("Filtrar")
        btn_filtrar.clicked.connect(self.atualizar)
        filtro_layout.addWidget(btn_filtrar)

        btn_todas = QPushButton("Ver todas")
        btn_todas.clicked.connect(self._ver_todas)
        filtro_layout.addWidget(btn_todas)

        filtro_layout.addStretch()

        self.label_total_dia = QLabel()
        self.label_total_dia.setStyleSheet("font-weight: bold; font-size: 14px; color: #145a32;")
        filtro_layout.addWidget(self.label_total_dia)

        layout.addLayout(filtro_layout)

        self.tabela = QTableWidget(0, 4)
        self.tabela.setHorizontalHeaderLabels(["ID", "Data/Hora", "Total", "Pagamento"])
        self.tabela.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabela.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tabela.doubleClicked.connect(self._ver_itens)
        layout.addWidget(self.tabela)

        dica = QLabel("Dica: dê duplo clique em uma venda para ver os itens.")
        dica.setStyleSheet("color: #7f8c8d; font-style: italic;")
        layout.addWidget(dica)

    def atualizar(self):
        data_inicio = self.data_inicio.date().toString("yyyy-MM-dd")
        data_fim = self.data_fim.date().toString("yyyy-MM-dd")
        vendas = self.db.listar_vendas(data_inicio, data_fim)
        self._preencher_tabela(vendas)
        self._atualizar_total_dia()

    def _ver_todas(self):
        vendas = self.db.listar_vendas()
        self._preencher_tabela(vendas)
        self._atualizar_total_dia()

    def _atualizar_total_dia(self):
        total = self.db.total_vendas_do_dia()
        self.label_total_dia.setText(f"Total vendido hoje: {fmt_moeda(total)}")

    def _preencher_tabela(self, vendas):
        self.tabela.setRowCount(0)
        for v in vendas:
            row = self.tabela.rowCount()
            self.tabela.insertRow(row)
            self.tabela.setItem(row, 0, QTableWidgetItem(str(v["id"])))
            self.tabela.setItem(row, 1, QTableWidgetItem(v["data_hora"]))
            self.tabela.setItem(row, 2, QTableWidgetItem(fmt_moeda(v["total"])))
            self.tabela.setItem(row, 3, QTableWidgetItem(v["forma_pagamento"]))

    def _ver_itens(self):
        row = self.tabela.currentRow()
        if row < 0:
            return
        venda_id = int(self.tabela.item(row, 0).text())
        dialogo = DialogItensVenda(self.db, venda_id, self)
        dialogo.exec()


# ---------------------------------------------------------------------------
# JANELA PRINCIPAL
# ---------------------------------------------------------------------------
class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema PDV")
        self.resize(1100, 650)

        self.db = Database()

        abas = QTabWidget()
        self.tab_historico = TabHistorico(self.db)
        self.tab_venda = TabVenda(self.db, atualizar_callback=self.tab_historico.atualizar)
        self.tab_produtos = TabProdutos(self.db)

        abas.addTab(self.tab_venda, "🛒 PDV (Venda)")
        abas.addTab(self.tab_produtos, "📦 Produtos")
        abas.addTab(self.tab_historico, "📊 Histórico")

        self.setCentralWidget(abas)

    def closeEvent(self, event):
        self.db.fechar()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
