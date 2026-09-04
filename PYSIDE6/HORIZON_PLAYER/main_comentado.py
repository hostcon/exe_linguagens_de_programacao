import os
import sys

# ============================================================================
# SEÇÃO 1 — IMPORTAÇÕES
# ============================================================================
# QtCore   -> classes "não visuais": tipos de dados, URLs, flags (Qt.*)
# QtMultimedia -> motor de áudio/vídeo (QMediaPlayer toca, QAudioOutput emite som)
# QtWidgets -> componentes visuais (janelas, botões, listas...)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStyle,
)

# Ui_MainWindow é a classe GERADA automaticamente a partir do interface.ui
# (Qt Designer) pelo compilador pyside6-uic. Ela nunca deve ser editada à mão:
# se você reabrir o interface.ui no Designer e salvar, este arquivo é
# regravado do zero e qualquer edição manual se perde.
from interface_ui import Ui_MainWindow


# ============================================================================
# SEÇÃO 2 — CLASSE PRINCIPAL DA JANELA
# ============================================================================
class HorizonPlayer(QMainWindow):
    """Classe principal da janela do player Horizon, herdando de QMainWindow."""

    # ------------------------------------------------------------------
    # 2.1 — INICIALIZAÇÃO (__init__)
    # ------------------------------------------------------------------
    def __init__(self):
        super().__init__()

        # Instancia a interface desenhada no Qt Designer (ver material em
        # anexo, seção "Composição vs Herança" para entender por que isto
        # NÃO é herança: HorizonPlayer só herda de QMainWindow).
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Configurações básicas da janela principal
        self.setWindowTitle("🎵 Horizon Media Player")

        # Estrutura de dados para armazenar a lista de músicas carregadas
        # Armazena dicionários no formato: {"nome": "musica.mp3", "caminho": "/caminho/musica.mp3"}
        self.playlist = []
        self.indice_atual = -1

        # ---------- Configuração do Motor de Áudio ----------
        # QMediaPlayer: Responsável pelo controle de estado (play, pause, seek, stop)
        self.player = QMediaPlayer(self)

        # QAudioOutput: Responsável pela saída física de áudio e controle de volume
        self.audio_output = QAudioOutput(self)
        self.player.setAudioOutput(self.audio_output)

        # Define volume padrão em 50% (faixa de 0.0 a 1.0)
        self.audio_output.setVolume(0.5)

        # Configura os ícones padrão do sistema nos botões
        self._configurar_icones()

        # Configura as conexões entre eventos da interface e métodos
        self._conectar_sinais()

    # ------------------------------------------------------------------
    # 2.2 — CONFIGURAÇÃO VISUAL (ícones nativos e sliders)
    # ------------------------------------------------------------------
    def _configurar_icones(self):
        """Define os ícones nativos do sistema operacional nos botões de controle."""
        estilo = self.style()
        self.ui.btn_abrir.setIcon(estilo.standardIcon(QStyle.SP_DirOpenIcon))
        self.ui.btn_retroceder.setIcon(
            estilo.standardIcon(QStyle.SP_MediaSeekBackward)
        )
        self.ui.btn_play.setIcon(estilo.standardIcon(QStyle.SP_MediaPlay))
        self.ui.btn_pause.setIcon(estilo.standardIcon(QStyle.SP_MediaPause))
        self.ui.btn_parar.setIcon(estilo.standardIcon(QStyle.SP_MediaStop))
        self.ui.btn_avancar.setIcon(
            estilo.standardIcon(QStyle.SP_MediaSeekForward)
        )

        # Configuração inicial dos sliders
        self.ui.slider_volume.setRange(0, 100)
        self.ui.slider_volume.setValue(50)
        self.ui.slider_posicao.setRange(0, 0)

    # ------------------------------------------------------------------
    # 2.3 — SINAIS E SLOTS (o "sistema nervoso" do programa)
    # ------------------------------------------------------------------
    def _conectar_sinais(self):
        """Mapeia os sinais (cliques, mudanças de valor) aos slots (funções)."""
        # Botões de ação
        self.ui.btn_abrir.clicked.connect(self.abrir_arquivos)
        self.ui.btn_play.clicked.connect(self.player.play)
        self.ui.btn_pause.clicked.connect(self.player.pause)
        self.ui.btn_parar.clicked.connect(self.player.stop)
        self.ui.btn_avancar.clicked.connect(self.avancar_10s)
        self.ui.btn_retroceder.clicked.connect(self.retroceder_10s)

        # Duplo clique em um item da lista de músicas
        self.ui.lista_musicas.itemDoubleClicked.connect(
            self.tocar_musica_selecionada
        )

        # Controle de volume: converte valor de 0-100 para float de 0.0-1.0
        self.ui.slider_volume.valueChanged.connect(
            lambda v: self.audio_output.setVolume(v / 100.0)
        )

        # Barra de progresso da música arrastada pelo usuário
        self.ui.slider_posicao.sliderMoved.connect(self.player.setPosition)

        # Atualizações emitidas pelo QMediaPlayer para refletir na interface
        self.player.positionChanged.connect(self.atualizar_posicao)
        self.player.durationChanged.connect(self.atualizar_duracao)
        self.player.mediaStatusChanged.connect(self.verificar_fim_da_faixa)

    # ========================================================================
    # SEÇÃO 3 — MÉTODOS DE CONTROLE (ações disparadas pelo usuário)
    # ========================================================================

    def abrir_arquivos(self):
        """Abre a caixa de diálogo permitindo selecionar múltiplos arquivos de áudio."""
        arquivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecionar Músicas",
            "",
            "Arquivos de Áudio (*.mp3 *.wav *.ogg *.flac *.m4a)",
        )

        if arquivos:
            for caminho in arquivos:
                nome_arquivo = os.path.basename(caminho)
                # Adiciona o item à estrutura interna
                self.playlist.append(
                    {"nome": nome_arquivo, "caminho": caminho}
                )
                # Adiciona o nome visível no QListWidget (com barra de rolagem nativa)
                self.ui.lista_musicas.addItem(f"🎵 {nome_arquivo}")

            # Se nenhuma música estava tocando, inicia automaticamente a primeira da fila
            if self.indice_atual == -1 and len(self.playlist) > 0:
                self.carregar_e_tocar(0)

    def carregar_e_tocar(self, indice):
        """Carrega a música do índice especificado no player e inicia a reprodução."""
        if 0 <= indice < len(self.playlist):
            self.indice_atual = indice
            item_musica = self.playlist[indice]

            # Define a fonte de áudio no QMediaPlayer através de uma QUrl local
            caminho_local = QUrl.fromLocalFile(item_musica["caminho"])
            self.player.setSource(caminho_local)

            # Atualiza o rótulo de texto na interface
            self.ui.label_musica.setText(f"🎶 Tocando: {item_musica['nome']}")

            # Destaca a linha correspondente no QListWidget
            self.ui.lista_musicas.setCurrentRow(indice)

            # Inicia o áudio
            self.player.play()

    def tocar_musica_selecionada(self):
        """Executa a música que recebeu o duplo clique na lista visual."""
        linha = self.ui.lista_musicas.currentRow()
        if linha >= 0:
            self.carregar_e_tocar(linha)

    # --------------------------------------------------------------------
    # avancar_10s / retroceder_10s
    #
    # COMO ESTÁ HOJE: os dois métodos abaixo fazem uma BUSCA POR TEMPO
    # (seek) dentro da MESMA faixa: somam/subtraem 10.000 ms da posição
    # atual do QMediaPlayer. Ou seja, "avançar" aqui não troca de música,
    # apenas pula 10s para frente/trás dentro da faixa que já está tocando.
    #
    # >>> COMO TRANSFORMAR EM "PRÓXIMA / ANTERIOR FAIXA" (apenas explicação,
    #     nenhuma linha de código abaixo é executada — são comentários) <<<
    #
    # A troca de "avançar tempo" para "avançar faixa" é simples porque o
    # método carregar_e_tocar(indice) já concentra toda a lógica de troca
    # de música (troca a fonte de áudio, atualiza o label, destaca a linha
    # na lista e dá play). Então os dois métodos passariam a apenas mover
    # o índice da playlist e delegar para ele, assim:
    #
    #     def avancar_10s(self):          # renomear para, por ex., proxima_musica
    #         proximo_indice = self.indice_atual + 1
    #         if proximo_indice < len(self.playlist):
    #             self.carregar_e_tocar(proximo_indice)
    #         # se quiser, trate aqui o caso "já é a última música"
    #         # (ex.: voltar para a primeira, ou simplesmente não fazer nada)
    #
    #     def retroceder_10s(self):       # renomear para, por ex., musica_anterior
    #         indice_anterior = self.indice_atual - 1
    #         if indice_anterior >= 0:
    #             self.carregar_e_tocar(indice_anterior)
    #         # idem: decidir o comportamento quando já é a primeira música
    #
    # Também seria interessante renomear as variáveis/ícones associados
    # (SP_MediaSkipForward / SP_MediaSkipBackward existem no QStyle e
    # combinam visualmente melhor com "próxima/anterior" do que os ícones
    # de "seek" usados hoje em _configurar_icones()).
    # --------------------------------------------------------------------
    def avancar_10s(self):
        """Pula a reprodução 10 segundos à frente."""
        nova_posicao = self.player.position() + 10_000  # Tempo em milissegundos
        self.player.setPosition(min(nova_posicao, self.player.duration()))

    def retroceder_10s(self):
        """Volta a reprodução 10 segundos atrás."""
        nova_posicao = self.player.position() - 10_000
        self.player.setPosition(max(nova_posicao, 0))

    # ========================================================================
    # SEÇÃO 4 — SINCRONIZAÇÃO DE INTERFACE (reagem a sinais do QMediaPlayer)
    # ========================================================================

    def atualizar_posicao(self, posicao_ms):
        """Sincroniza o slider e o tempo decorrido conforme a música avança."""
        # Evita conflito visual caso o usuário esteja arrastando o slider
        if not self.ui.slider_posicao.isSliderDown():
            self.ui.slider_posicao.setValue(posicao_ms)
        self.ui.label_tempo_atual.setText(self.formatar_tempo(posicao_ms))

    def atualizar_duracao(self, duracao_ms):
        """Ajusta o limite máximo do slider quando a duração total é identificada."""
        self.ui.slider_posicao.setRange(0, duracao_ms)
        self.ui.label_tempo_total.setText(self.formatar_tempo(duracao_ms))

    def verificar_fim_da_faixa(self, status):
        """Avança para a próxima música da playlist quando a faixa atual terminar."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            proximo_indice = self.indice_atual + 1
            if proximo_indice < len(self.playlist):
                self.carregar_e_tocar(proximo_indice)
            else:
                # Fim da lista atingido
                self.player.stop()

    # --------------------------------------------------------------------
    # NOVA FUNCIONALIDADE (apenas explicação em comentário): excluir uma
    # ou VÁRIAS músicas da lista, incluindo um atalho para selecionar
    # tudo (Ctrl+A) e apagar de uma vez com Delete.
    #
    # Pré-requisito: por padrão o QListWidget só permite selecionar UM
    # item por vez. Para permitir selecionar vários (com Ctrl+clique,
    # Shift+clique ou "selecionar tudo"), é preciso trocar o modo de
    # seleção — normalmente dentro de _configurar_icones() ou logo no
    # __init__, uma única vez:
    #
    #     from PySide6.QtWidgets import QAbstractItemView  # import extra necessário
    #     self.ui.lista_musicas.setSelectionMode(QAbstractItemView.ExtendedSelection)
    #
    # QMainWindow (e qualquer QWidget) já recebe eventos de teclado através
    # do método keyPressEvent(self, event), que por padrão não faz nada de
    # especial. Para reagir à tecla Delete (removendo um OU vários itens
    # selecionados) e ao atalho Ctrl+A (selecionar tudo), basta SOBRESCREVER
    # esse método dentro da classe HorizonPlayer:
    #
    #     def keyPressEvent(self, event):
    #         lista = self.ui.lista_musicas
    #
    #         if event.key() == Qt.Key_Delete and lista.hasFocus():
    #             # pega TODAS as linhas selecionadas (pode ser uma ou várias)
    #             # e ordena em ordem DECRESCENTE: isso é essencial, porque
    #             # remover de trás para frente evita que os índices das
    #             # linhas ainda não removidas se desloquem no meio do laço
    #             linhas_selecionadas = sorted(
    #                 {indice.row() for indice in lista.selectedIndexes()},
    #                 reverse=True,
    #             )
    #             musica_atual_foi_removida = False
    #
    #             for linha in linhas_selecionadas:
    #                 lista.takeItem(linha)          # remove visualmente
    #                 del self.playlist[linha]        # remove da estrutura de dados
    #
    #                 if linha == self.indice_atual:
    #                     musica_atual_foi_removida = True
    #                 elif linha < self.indice_atual:
    #                     # uma música ANTES da atual foi removida:
    #                     # o índice da atual precisa "andar" pra trás
    #                     self.indice_atual -= 1
    #
    #             if musica_atual_foi_removida:
    #                 # a música que tocava foi apagada (ou fazia parte do
    #                 # "selecionar tudo") — para o player com segurança
    #                 self.player.stop()
    #                 self.indice_atual = -1
    #                 self.ui.label_musica.setText("Nenhuma música carregada")
    #
    #         elif (
    #             event.key() == Qt.Key_A
    #             and event.modifiers() == Qt.ControlModifier
    #             and lista.hasFocus()
    #         ):
    #             # Ctrl+A: seleciona todos os itens da lista de uma vez.
    #             # selectAll() já vem pronto de QAbstractItemView (superclasse
    #             # de QListWidget) — não precisa reimplementar nada, só chamar.
    #             lista.selectAll()
    #
    #         else:
    #             # qualquer outra tecla segue o comportamento padrão do Qt
    #             super().keyPressEvent(event)
    #
    # (Qt.Key_Delete, Qt.Key_A e Qt.ControlModifier já estão disponíveis
    # pois "Qt" é importado no topo do arquivo, de PySide6.QtCore.)
    # --------------------------------------------------------------------

    # ========================================================================
    # SEÇÃO 5 — MÉTODOS UTILITÁRIOS
    # ========================================================================
    @staticmethod
    def formatar_tempo(milissegundos):
        """Converte milissegundos inteiros no formato legível MM:SS."""
        segundos = milissegundos // 1000
        minutos = segundos // 60
        segundos_restantes = segundos % 60
        return f"{minutos:02d}:{segundos_restantes:02d}"


# ============================================================================
# SEÇÃO 6 — PONTO DE ENTRADA DA APLICAÇÃO
# ============================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Carrega a folha de estilos caso o arquivo exista
    if os.path.exists("style.qss"):
        with open("style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    janela = HorizonPlayer()
    janela.show()
    sys.exit(app.exec())
