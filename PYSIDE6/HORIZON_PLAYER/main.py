import os
import sys

# Importação dos módulos do PySide6
from PySide6.QtCore import Qt, QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QStyle,
)

# Importação da interface gráfica gerada a partir do Qt Designer
from interface_ui import Ui_MainWindow


class HorizonPlayer(QMainWindow):
    """Classe principal da janela do player Horizon, herdando de QMainWindow."""

    def __init__(self):
        super().__init__()

        # Instancia e configura a interface desenhada no Qt Designer
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

    # ==================== MÉTODOS DE CONTROLE ====================

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

    def avancar_10s(self):
        """Pula a reprodução 10 segundos à frente."""
        nova_posicao = self.player.position() + 10_000  # Tempo em milissegundos
        self.player.setPosition(min(nova_posicao, self.player.duration()))

    def retroceder_10s(self):
        """Volta a reprodução 10 segundos atrás."""
        nova_posicao = self.player.position() - 10_000
        self.player.setPosition(max(nova_posicao, 0))

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

    @staticmethod
    def formatar_tempo(milissegundos):
        """Converte milissegundos inteiros no formato legível MM:SS."""
        segundos = milissegundos // 1000
        minutos = segundos // 60
        segundos_restantes = segundos % 60
        return f"{minutos:02d}:{segundos_restantes:02d}"


# ==================== PONTO DE ENTRADA ====================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Carrega a folha de estilos caso o arquivo exista
    if os.path.exists("style.qss"):
        with open("style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            
    janela = HorizonPlayer()
    janela.show()
    sys.exit(app.exec())

