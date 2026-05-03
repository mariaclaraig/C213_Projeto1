from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from backend.utils.data_loader import carregar_mat
from backend.models.identificacao import identificar_sistemas
from backend.models.sintonia import sintonizar_chr, sintonizar_cc, sintonizar_manual, validar_estabilidade
from backend.utils.simulation import simular_malha_fechada


class AppController(QObject):

    dados_carregados      = pyqtSignal(dict)   # após carregar .mat
    identificacao_pronta  = pyqtSignal(dict)   # após rodar Smith
    sintonia_pronta       = pyqtSignal(dict)   # após calcular Kp, Ti, Td
    simulacao_pronta      = pyqtSignal(dict)   # após simular malha fechada
    erro_ocorrido         = pyqtSignal(str)    # mensagem de erro para a GUI

    def __init__(self, view=None):
        super().__init__()
        self.view = view
        self._dados   = None   # dados do .mat carregado
        self._modelo  = None   # {k, tau, theta, eqm, ...}
        self._pid     = None   # {Kp, Ti, Td}
        self._metodo  = 'CHR'  # método de sintonia ativo

    def on_escolher_arquivo(self):

        caminho, _ = QFileDialog.getOpenFileName(
            None, "Selecionar Dataset", "", "MATLAB Files (*.mat)"
        )
        if not caminho:
            return
        try:
            self._dados = carregar_mat(caminho)
            self.dados_carregados.emit(self._dados)
        except Exception as e:
            self.erro_ocorrido.emit(str(e))

    def on_identificar(self):
    
        if self._dados is None:
            self.erro_ocorrido.emit("Nenhum dataset carregado.")
            return
        try:
            modelos = identificar_sistemas(
                self._dados['t'],
                self._dados['y'],
                self._dados['u']
            )
            self._modelo = modelos['smith']
            self.identificacao_pronta.emit(self._modelo)
        except Exception as e:
            self.erro_ocorrido.emit(f"Erro na identificação: {str(e)}")

    def on_sintonizar(self, metodo='CHR', Kp=None, Ti=None, Td=None):
        
        if self._modelo is None:
            self.erro_ocorrido.emit("Identificação não realizada.")
            return

        k   = self._modelo['k']
        tau = self._modelo['tau']
        theta = self._modelo['theta']

        try:
            if metodo == 'CHR':
                self._pid = sintonizar_chr(k, tau, theta)
            elif metodo == 'CC':
                self._pid = sintonizar_cc(k, tau, theta)
            elif metodo == 'Manual':
                if None in (Kp, Ti, Td):
                    self.erro_ocorrido.emit("Preencha Kp, Ti e Td para o modo Manual.")
                    return
                estavel, msg = validar_estabilidade(k, tau, theta, Kp, Ti, Td)
                if not estavel:
                    self.erro_ocorrido.emit(f"Sistema instável: {msg}")
                    return
                self._pid = sintonizar_manual(Kp, Ti, Td)
            else:
                self.erro_ocorrido.emit(f"Método desconhecido: {metodo}")
                return

            self._metodo = metodo
            self.sintonia_pronta.emit(self._pid)

        except Exception as e:
            self.erro_ocorrido.emit(f"Erro na sintonia: {str(e)}")

    def on_simular(self, setpoint):

        if self._modelo is None or self._pid is None:
            self.erro_ocorrido.emit("Realize a identificação e sintonia antes de simular.")
            return
        try:
            resultado = simular_malha_fechada(
                k=self._modelo['k'],
                tau=self._modelo['tau'],
                theta=self._modelo['theta'],
                Kp=self._pid['Kp'],
                Ti=self._pid['Ti'],
                Td=self._pid['Td'],
                setpoint=float(setpoint)
            )
            self.simulacao_pronta.emit(resultado)
        except Exception as e:
            self.erro_ocorrido.emit(f"Erro na simulação: {str(e)}")

    def get_dados(self):
        return self._dados

    def get_modelo(self):
        return self._modelo

    def get_pid(self):
        return self._pid

    def get_setpoint_inicial(self):
        
        if self._dados is not None:
            return float(self._dados['y'][-1])
        return 1.0
