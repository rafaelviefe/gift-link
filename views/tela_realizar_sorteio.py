from typing import List

import FreeSimpleGUI as sg

from controller.participante_controller import ParticipanteController
from controller.sorteio_controller import SorteioController
from model.evento import Evento
from model.organizador import Organizador
from model.participante import Participante
from views.theme import configure_theme


class TelaRealizarSorteio:
    def __init__(self, evento: Evento, organizador: Organizador):
        configure_theme()
        self.__evento = evento
        self.__organizador = organizador
        self.__sorteio_controller = SorteioController()
        self.__participante_controller = ParticipanteController()
        self.__participantes_elegiveis: List[Participante] = []
        self.__janela = None

    def __obter_participantes(self):
        # Busca todos e filtra apenas os elegíveis (regra de negócio: senha alterada)
        todos, _ = self.__participante_controller.listar()
        self.__participantes_elegiveis = [p for p in todos if p.is_elegivel()]

    def __criar_janela(self):
        self.__obter_participantes()

        # Tabela com Checkboxes (simulado com seleção múltipla ou coluna extra)
        # Vamos usar uma Listbox com select_mode multiple para facilitar a seleção
        lista_nomes = [f"{p.get_id()} - {p.get_username()}" for p in self.__participantes_elegiveis]

        layout = [
            [sg.Text(f"Sorteio: {self.__evento.get_nome()}", font=("Helvetica", 18, "bold"))],
            [sg.Text(f"Min: {self.__evento.get_min_participantes()} | Max: {self.__evento.get_max_participantes()}")],
            [sg.Text("Selecione os participantes para o sorteio (CTRL+Click para selecionar vários):")],
            [
                sg.Listbox(
                    values=lista_nomes,
                    select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                    size=(40, 10),
                    key="-SELECAO-",
                    font=("Helvetica", 12)
                )
            ],
            [sg.Text("", key="-MSG-", text_color="yellow")],
            [sg.Button("CONFIRMAR SORTEIO", key="-SORTEAR-", button_color=("white", "green")), sg.Button("Voltar", key="-VOLTAR-")]
        ]

        return sg.Window("Realizar Sorteio - GiftLink", layout, finalize=True, element_justification="center")

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evt, valores = self.__janela.read()

            if evt == sg.WIN_CLOSED or evt == "-VOLTAR-":
                self.fechar()
                return "menu_eventos", self.__organizador, None

            if evt == "-SORTEAR-":
                selecionados_str = valores["-SELECAO-"]

                # Converter strings da listbox de volta para objetos Participante
                participantes_escolhidos = []
                for item_str in selecionados_str:
                    p_id = int(item_str.split(" - ")[0])
                    for p in self.__participantes_elegiveis:
                        if p.get_id() == p_id:
                            participantes_escolhidos.append(p)
                            break

                # Chama o controller para validar e sortear
                sucesso, msg = self.__sorteio_controller.realizar_sorteio(self.__evento, participantes_escolhidos)

                if sucesso:
                    sg.popup(msg)
                    self.fechar()
                    return "menu_eventos", self.__organizador, None
                else:
                    self.__janela["-MSG-"].update(msg)
                    sg.popup_error(msg)

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None
