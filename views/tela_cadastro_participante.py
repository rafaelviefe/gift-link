import FreeSimpleGUI as sg
from views.theme import configure_theme
from typing import Iterable
from controller.participante_controller import ParticipanteController
from model.organizador import Organizador

class TelaCadastroParticipante:
    def __init__(self, participante_controller: ParticipanteController, organizador: Organizador):
        configure_theme()
        self.__participante_controller = participante_controller
        self.__organizador = organizador
        self.__janela = None

    def _format_participantes(self, participantes: Iterable) -> list:
        rows = []
        if not participantes:
            return rows
        for p in participantes:
            pid = p.get_id()
            username = p.get_username()
            eleg = "Sim" if p.is_elegivel() else "Não"
            rows.append([pid, username, eleg])
        return rows

    def __criar_janela(self):
        participantes, _ = self.__participante_controller.listar_participantes()
        
        headings = ["ID", "Username", "Elegível"]
        table_values = self._format_participantes(participantes)

        layout = [
            [sg.Text("Cadastro de Participante", font=("Helvetica", 20, "bold"))],
            [sg.Text("Username", size=(14, 1)), sg.InputText(key="-USERNAME-")],
            [
                sg.Table(
                    values=table_values,
                    headings=headings,
                    auto_size_columns=False,
                    col_widths=[8, 30, 12],
                    justification="center",
                    num_rows=10,
                    key="-TABLE-",
                )
            ],
            [sg.Button("Cadastrar", key="-SUBMIT-"), sg.Button("Voltar", key="-VOLTAR-")],
        ]
        return sg.Window(
            "Cadastro de Participantes - GiftLink", layout, finalize=True, element_justification="center"
        )

    def __atualizar_tabela(self):
        if not self.__janela:
            return
        participantes, _ = self.__participante_controller.listar_participantes()
        rows = self._format_participantes(participantes)
        self.__janela["-TABLE-"].update(values=rows)

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == "-VOLTAR-":
                self.fechar()
                return "painel_organizador", self.__organizador, None
            
            if evento == "-SUBMIT-":
                username = valores["-USERNAME-"]
                _, mensagem = self.__participante_controller.registrar_participante(username)
                sg.popup(mensagem)
                self.__janela["-USERNAME-"].update("")
                self.__atualizar_tabela()

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None