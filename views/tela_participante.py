import FreeSimpleGUI as sg
from views.theme import configure_theme
from model.participante import Participante

class TelaParticipante:
    def __init__(self, participante: Participante):
        configure_theme()
        self.__participante = participante
        self.__janela = None

    def __criar_janela(self):
        layout = [
            [
                sg.Text(
                    f"Bem-vindo, {self.__participante.get_username()}!",
                    font=("Helvetica", 20, "bold"),
                )
            ],
            [sg.VPush()],
            [sg.Button("Visualizar Eventos", key="-MEUSEVENTOS-")],
            [sg.Button("Lista de Desejos", key="-DESEJOS-")],
            [sg.Button("Logout", key="-LOGOUT-")],
            [sg.VPush()],
        ]
        return sg.Window(
            f"Painel do Participante - {self.__participante.get_username()}",
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
            
            if evento in ["-MEUSEVENTOS-", "-DESEJOS-"]:
                sg.popup(f"Funcionalidade de '{evento.strip('-')}' será implementada em breve!")

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None