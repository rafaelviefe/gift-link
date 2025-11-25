import FreeSimpleGUI as sg
from views.theme import configure_theme
from model.organizador import Organizador

class TelaEventosMenu:
    def __init__(self, organizador: Organizador):
        configure_theme()
        self.__organizador = organizador
        self.__janela = None
    
    def __criar_janela(self):
        layout = [
            [sg.Text("Gerenciar Eventos", font=("Helvetica", 20, "bold"))],
            [sg.VPush()],
            [sg.Button("Cadastrar Novo Evento", key="-CADASTRO_EVENTO-", size=(25, 2))],
            [sg.Text("")],
            [sg.Button("Gerenciar Participantes", key="-GERENCIAR_PARTICIPANTES-", size=(25, 2))],
            [sg.VPush()],
            [sg.Button("Voltar", key="-VOLTAR-")]
        ]
        return sg.Window(
            "Menu de Eventos",
            layout,
            finalize=True,
            element_justification="center",
            size=(400, 350),
        )

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == "-VOLTAR-":
                self.fechar()
                return "painel_organizador", self.__organizador, None
            
            if evento == '-CADASTRO_EVENTO-':
                self.fechar()
                return "cadastro_evento", self.__organizador, None
            
            if evento == '-GERENCIAR_PARTICIPANTES-':
                self.fechar()
                return "selecionar_evento_participacao", self.__organizador, None

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None