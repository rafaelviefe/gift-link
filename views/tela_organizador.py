import FreeSimpleGUI as sg

from model.organizador import Organizador
from views.theme import configure_theme


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
                    font=("Helvetica", 24, "bold"),
                )
            ],
            [sg.VPush()],
            [sg.Button("Participantes", key="-PARTICIPANTES-", size=(20, 2), font=("Helvetica", 14))],
            [sg.Text("")],  # Espaçamento
            [sg.Button("Eventos", key="-EVENTOS-", size=(20, 2), font=("Helvetica", 14))],
            [sg.Text("")],  # Espaçamento
            [sg.Button("Sorteios", key="-SORTEIOS-", size=(20, 2), font=("Helvetica", 14))],
            [sg.Text("")],  # Espaçamento
            [sg.Button("Logout", key="-LOGOUT-", size=(20, 2), font=("Helvetica", 14), button_color=("white", "#d9534f"))],
            [sg.VPush()],
        ]
        return sg.Window(
            f"Painel do Organizador - {self.__organizador.get_username()}",
            layout,
            finalize=True,
            element_justification="center",
            size=(700, 600),
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
                self.fechar()
                return "gerenciar_eventos", None, None

            if evento == '-SORTEIOS-': # Tratamento do novo botão
                self.fechar()
                return "menu_sorteios", self.__organizador, None

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None
