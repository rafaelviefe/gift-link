from typing import List, Optional

import FreeSimpleGUI as sg

from controller.evento_controller import EventoController
from model.evento import Evento
from model.organizador import Organizador
from views.theme import configure_theme


class TelaListaSorteios:
    def __init__(self, organizador: Organizador):
        configure_theme()
        self.__organizador = organizador
        self.__evento_controller = EventoController()
        self.__eventos: List[Evento] = []
        self.__janela = None

    def _format_eventos(self) -> list:
        # Busca eventos para listar na tabela
        rows = []
        self.__eventos, _ = self.__evento_controller.listar()
        if not self.__eventos:
            return rows
        for e in self.__eventos:
            # Filtra apenas eventos do organizador logado, se desejar
            if e.get_organizador().get_username() == self.__organizador.get_username():
                rows.append([e.get_id(), e.get_nome(), e.get_status().value])
        return rows

    def __criar_janela(self):
        headings = ["ID", "Nome", "Status"]
        table_values = self._format_eventos()

        layout = [
            [sg.Text("Central de Sorteios", font=("Helvetica", 20, "bold"))],
            [sg.Text("Selecione um evento para realizar ou visualizar o sorteio:")],
            [
                sg.Table(
                    values=table_values,
                    headings=headings,
                    auto_size_columns=False,
                    col_widths=[5, 30, 15],
                    justification="center",
                    num_rows=10,
                    key="-TABLE-",
                    enable_events=True,
                    select_mode=sg.TABLE_SELECT_MODE_BROWSE
                )
            ],
            [sg.Button("Abrir Sorteio", key="-ABRIR-", disabled=True)],
            [sg.Button("Voltar", key="-VOLTAR-")]
        ]
        return sg.Window(
            "Lista de Sorteios - GiftLink",
            layout,
            finalize=True,
            element_justification="center"
        )

    def abrir(self):
        self.__janela = self.__criar_janela()
        evento_selecionado = None

        while True:
            evt, valores = self.__janela.read()

            if evt == sg.WIN_CLOSED or evt == "-VOLTAR-":
                self.fechar()
                return "painel_organizador", self.__organizador, None

            if evt == "-TABLE-" and valores["-TABLE-"]:
                # Habilita o botão quando uma linha é selecionada
                indice = valores["-TABLE-"][0]
                # Precisamos mapear o índice da tabela para a lista filtrada corretamente
                # OBS: A lógica abaixo assume que a lista self.__eventos contém o que está na tabela.
                # Se houver filtro no _format_eventos, certifique-se de que a lista self.__eventos esteja sincronizada.
                # Para simplificar, vou refazer a lista filtrada aqui ou usar o ID da linha se possível.

                # Forma segura: Pegar o ID da linha selecionada nos values (se configurado) ou pelo indice
                # Vamos reconstruir a lista localmente para garantir o índice:
                eventos_filtrados = [e for e in self.__eventos if e.get_organizador().get_username() == self.__organizador.get_username()]
                if indice < len(eventos_filtrados):
                    evento_selecionado = eventos_filtrados[indice]
                    self.__janela["-ABRIR-"].update(disabled=False)

            if evt == "-ABRIR-":
                if evento_selecionado:
                    self.fechar()
                    return "acao_sorteio", evento_selecionado, None

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None
