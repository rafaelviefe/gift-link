import FreeSimpleGUI as sg
from controller.evento_controller import EventoController
from model.organizador import Organizador
from views.theme import configure_theme

class TelaSelecionarEvento:
    def __init__(self, organizador: Organizador):
        configure_theme()
        self.__organizador = organizador
        self.__evento_controller = EventoController()
        self.__eventos = []
        self.__janela = None

    def __criar_janela(self):
        self.__eventos, _ = self.__evento_controller.listar()
        eventos_filtrados = [e for e in self.__eventos if e.get_organizador().get_username() == self.__organizador.get_username()]
        self.__eventos = eventos_filtrados

        nomes_eventos = [f"{e.get_id()} - {e.get_nome()} ({e.get_status().value})" for e in self.__eventos]

        layout = [
            [sg.Text("Selecione um Evento", font=("Helvetica", 18, "bold"))],
            [sg.Listbox(values=nomes_eventos, size=(40, 10), key="-LISTA-", enable_events=True)],
            [sg.Button("Selecionar", key="-OK-", disabled=True), sg.Button("Voltar", key="-VOLTAR-")]
        ]
        
        return sg.Window("Seleção de Evento - GiftLink", layout, finalize=True, element_justification="center")

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evt, valores = self.__janela.read()

            if evt == sg.WIN_CLOSED or evt == "-VOLTAR-":
                self.fechar()
                return "voltar", None, None

            if evt == "-LISTA-" and valores["-LISTA-"]:
                self.__janela["-OK-"].update(disabled=False)

            if evt == "-OK-":
                selecao = valores["-LISTA-"]
                if selecao:
                    indice = self.__janela["-LISTA-"].get_indexes()[0]
                    evento_selecionado = self.__eventos[indice]
                    self.fechar()
                    return "evento_selecionado", evento_selecionado, None

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None