import FreeSimpleGUI as sg
from views.theme import configure_theme
from model.organizador import Organizador
from controller.participante_controller import ParticipanteController

class TelaOrganizador:
    def __init__(self, organizador: Organizador):
        configure_theme()
        self.__organizador = organizador
        self.__janela = None
    
    def __criar_janela(self):
        layout = [
            [
                sg.Text(
                    f"Bem-vindo, {self.__organizador.get_username()}!",
                    font=("Helvetica", 20, "bold"),
                )
            ],
            [sg.VPush()],
            [sg.Button("Participantes", key="-PARTICIPANTES-")],
            [sg.Button("Eventos", key="-EVENTOS-")],
            [sg.Button("Logout", key="-LOGOUT-")],
            [sg.VPush()],
        ]
        return sg.Window(
            f"Painel do Organizador - {self.__organizador.get_username()}",
            layout,
            finalize=True,
            element_justification="center",
            size=(500, 400),
        )

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED:
                self.fechar()
                return "sair", None, None
            
            if evento == '-LOGOUT-':
                self.fechar()
                return "logout", None, None

            if evento == '-PARTICIPANTES-':
                self.fechar()
                return "gerenciar_participantes", None, None
            
            if evento == '-EVENTOS-':
                sg.popup(f"Funcionalidade de '{evento.strip('-')}' será implementada em breve!")

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None