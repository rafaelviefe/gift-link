from typing import Iterable, List, Optional

import FreeSimpleGUI as sg

from controller.evento_controller import EventoController
from model.evento import Evento
from model.organizador import Organizador
from views.theme import configure_theme


class TelaCadastroEvento:
    def __init__(self, evento_controller: EventoController, organizador: Organizador):
        configure_theme()
        self.__evento_controller = evento_controller
        self.__organizador = organizador
        self.__eventos: List[Evento] = []
        self.__janela = None

    def _format_eventos(self) -> list:
        rows = []
        self.__eventos, _ = self.__evento_controller.listar()
        if not self.__eventos:
            return rows
        for e in self.__eventos:
            rows.append(
                [
                    e.get_id(),
                    e.get_nome(),
                    e.get_descricao(),
                    e.get_min_participantes(),
                    e.get_max_participantes(),
                    e.get_status().value,
                    e.get_organizador().get_username(),
                ]
            )
        return rows

    def __layout_aba_cadastro(self):
        return [
            [sg.Text("Nome:", size=(10, 1)), sg.InputText(key="-NOME-")],
            [sg.Text("Descrição:", size=(10, 1)), sg.InputText(key="-DESCRICAO-")],
            [
                sg.Text("Min Part:", size=(10, 1)),
                sg.InputText(key="-MIN_PART-", size=(10, 1), tooltip="Digite apenas números inteiros"),
                sg.Text("Max Part:", size=(10, 1)),
                sg.InputText(key="-MAX_PART-", size=(10, 1), tooltip="Digite apenas números inteiros"),
            ],
            [sg.Text("", key="-MSG_CADASTRO-", text_color="red", size=(50, 1))],
            [sg.Button("Cadastrar Evento", key="-SUBMIT_CADASTRO-")],
        ]

    def __layout_aba_edicao(self):
        return [
            [sg.Text("Selecione um evento na tabela para editar.", key="-EDIT_TEXT-")],
            [
                sg.Text("Nome:", size=(10, 1)),
                sg.InputText(key="-NOME_EDIT-", disabled=True),
            ],
            [
                sg.Text("Descrição:", size=(10, 1)),
                sg.InputText(key="-DESCRICAO_EDIT-", disabled=True),
            ],
            [
                sg.Text("Outros campos não são editáveis.", font=("Helvetica", 10, "italic"))
            ],
            [
                sg.Button("Salvar Edição", key="-SUBMIT_EDICAO-", disabled=True),
                sg.Button("Cancelar Edição", key="-CANCEL_EDICAO-", disabled=True),
            ],
        ]

    def __criar_janela(self):
        headings = ["ID", "Nome", "Descrição", "Min", "Max", "Status", "Organizador"]
        table_values = self._format_eventos()

        layout_tabela = [
            [
                sg.Table(
                    values=table_values,
                    headings=headings,
                    auto_size_columns=False,
                    col_widths=[5, 20, 30, 5, 5, 15, 15],
                    justification="center",
                    num_rows=10,
                    key="-TABLE-",
                    enable_events=True,
                )
            ],
        ]

        layout_abas = [
            [
                sg.TabGroup(
                    [
                        [
                            sg.Tab("Cadastrar", self.__layout_aba_cadastro()),
                            sg.Tab("Editar", self.__layout_aba_edicao()),
                        ]
                    ],
                    key="-TAB_GROUP-",
                )
            ]
        ]

        layout = [
            [sg.Text("Gerenciamento de Eventos", font=("Helvetica", 20, "bold"))],
            [sg.Frame("Eventos Existentes", layout_tabela)],
            [sg.Frame("Ações", layout_abas)],
            [sg.Button("Voltar", key="-VOLTAR-")],
        ]
        return sg.Window(
            "Cadastro de Eventos - GiftLink",
            layout,
            finalize=True,
            element_justification="center",
        )

    def __atualizar_tabela(self):
        if not self.__janela:
            return
        rows = self._format_eventos()
        self.__janela["-TABLE-"].update(values=rows)

    def __limpar_campos_cadastro(self):
        self.__janela["-NOME-"].update("")
        self.__janela["-DESCRICAO-"].update("")
        self.__janela["-MIN_PART-"].update("")
        self.__janela["-MAX_PART-"].update("")
        self.__janela["-MSG_CADASTRO-"].update("")

    def __obter_evento_selecionado(self, valores) -> Optional[Evento]:
        try:
            indices_selecionados = valores["-TABLE-"]
            if not indices_selecionados:
                return None

            indice_evento = indices_selecionados[0]
            evento_selecionado = self.__eventos[indice_evento]
            return evento_selecionado
        except Exception:
            return None

    def __habilitar_edicao(self, evento: Evento):
        self.__janela["-NOME_EDIT-"].update(evento.get_nome(), disabled=False)
        self.__janela["-DESCRICAO_EDIT-"].update(evento.get_descricao(), disabled=False)
        self.__janela["-SUBMIT_EDICAO-"].update(disabled=False)
        self.__janela["-CANCEL_EDICAO-"].update(disabled=False)
        self.__janela["-EDIT_TEXT-"].update(f"Editando Evento ID: {evento.get_id()}")
        self.__janela["-TAB_GROUP-"].Widget.select(1)

    def __desabilitar_edicao(self):
        self.__janela["-NOME_EDIT-"].update("", disabled=True)
        self.__janela["-DESCRICAO_EDIT-"].update("", disabled=True)
        self.__janela["-SUBMIT_EDICAO-"].update(disabled=True)
        self.__janela["-CANCEL_EDICAO-"].update(disabled=True)
        self.__janela["-EDIT_TEXT-"].update("Selecione um evento na tabela para editar.")

    def abrir(self):
        self.__janela = self.__criar_janela()
        evento_em_edicao = None

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == "-VOLTAR-":
                self.fechar()
                return "menu_eventos", self.__organizador, None

            if evento == "-SUBMIT_CADASTRO-":
                nome = valores["-NOME-"]
                descricao = valores["-DESCRICAO-"]
                min_part_str = valores["-MIN_PART-"].strip()
                max_part_str = valores["-MAX_PART-"].strip()

                # Validação de entrada antes de enviar ao controller
                try:
                    if not min_part_str or not max_part_str:
                        self.__janela["-MSG_CADASTRO-"].update("Por favor, preencha os campos de mínimo e máximo de participantes.")
                        sg.popup_error("Por favor, preencha os campos de mínimo e máximo de participantes.")
                        continue

                    min_part = int(min_part_str)
                    max_part = int(max_part_str)
                except ValueError:
                    self.__janela["-MSG_CADASTRO-"].update("⚠️ Os valores devem ser números inteiros válidos (ex: 2, 10, 20)")
                    sg.popup_error("Os valores de mínimo e máximo de participantes devem ser números inteiros válidos.\n\nExemplos válidos: 2, 4, 10, 20")
                    continue

                # Limpa mensagem de erro se passou na validação
                self.__janela["-MSG_CADASTRO-"].update("")

                _, mensagem = self.__evento_controller.registrar(
                    nome, descricao, min_part, max_part, self.__organizador
                )
                sg.popup(mensagem)
                self.__limpar_campos_cadastro()
                self.__atualizar_tabela()

            if evento == "-TABLE-":
                evento_em_edicao = self.__obter_evento_selecionado(valores)
                if evento_em_edicao:
                    self.__habilitar_edicao(evento_em_edicao)
                else:
                    self.__desabilitar_edicao()

            if evento == "-SUBMIT_EDICAO-":
                if evento_em_edicao:
                    novo_nome = valores["-NOME_EDIT-"]
                    nova_descricao = valores["-DESCRICAO_EDIT-"]

                    _, msg = self.__evento_controller.editar(evento_em_edicao, novo_nome, nova_descricao)
                    sg.popup(msg)

                    evento_em_edicao = None
                    self.__desabilitar_edicao()
                    self.__atualizar_tabela()

            if evento == "-CANCEL_EDICAO-":
                evento_em_edicao = None
                self.__desabilitar_edicao()

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None
