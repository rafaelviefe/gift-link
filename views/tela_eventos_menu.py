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
            [
                sg.Text(
                    "Gerenciar Eventos",
                    font=("Helvetica", 20, "bold"),
                )
            ],
            [sg.VPush()],
            [sg.Button("Cadastrar", key="-CADASTRO_EVENTO-")],
            [sg.Button("Detalhes", key="-DETALHES_EVENTO-")],
            [sg.Button("Voltar", key="-VOLTAR-")],
            [sg.VPush()],
        ]
        return sg.Window(
            "Menu de Eventos",
            layout,
            finalize=True,
            element_justification="center",
            size=(500, 400),
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
            
            if evento == '-DETALHES_EVENTO-':
                sg.popup(f"Funcionalidade de '{evento.strip('-')}' estará disponível em breve!")

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None