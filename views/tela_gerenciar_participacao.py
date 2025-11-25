import FreeSimpleGUI as sg
from controller.participante_controller import ParticipanteController
from controller.participacao_controller import ParticipacaoController
from model.evento import Evento
from model.organizador import Organizador
from views.theme import configure_theme

class TelaGerenciarParticipacao:
    def __init__(self, evento: Evento, organizador: Organizador):
        configure_theme()
        self.__evento = evento
        self.__organizador = organizador
        self.__participante_controller = ParticipanteController()
        self.__participacao_controller = ParticipacaoController()
        self.__todos_participantes = []
        self.__ids_no_evento = []
        self.__janela = None

    def __carregar_dados(self):
        todos, _ = self.__participante_controller.listar()
        self.__todos_participantes = [p for p in todos if p.is_elegivel()]
        
        participantes_evento, _ = self.__participacao_controller.listar_participantes_do_evento(self.__evento.get_id())
        self.__ids_no_evento = [p.get_id() for p in participantes_evento]

    def __criar_janela(self):
        self.__carregar_dados()

        linhas_participantes = []
        for p in self.__todos_participantes:
            esta_no_evento = p.get_id() in self.__ids_no_evento
            linhas_participantes.append(
                [sg.Checkbox(f"{p.get_username()} (ID: {p.get_id()})", default=esta_no_evento, key=f"-P_{p.get_id()}-")]
            )

        layout_lista = [
            [sg.Column(linhas_participantes, scrollable=True, vertical_scroll_only=True, size=(350, 200))]
        ]

        layout = [
            [sg.Text(f"Gerenciar: {self.__evento.get_nome()}", font=("Helvetica", 16, "bold"))],
            [sg.Text("Marque os participantes que estarão neste evento:")],
            [sg.Frame("Participantes Elegíveis", layout_lista)],
            [sg.Button("Salvar Alterações", key="-SALVAR-"), sg.Button("Voltar", key="-VOLTAR-")]
        ]

        return sg.Window("Gerenciar Participantes - GiftLink", layout, finalize=True, element_justification="center")

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evt, valores = self.__janela.read()

            if evt == sg.WIN_CLOSED or evt == "-VOLTAR-":
                self.fechar()
                return "menu_eventos", self.__organizador, None

            if evt == "-SALVAR-":
                alteracoes_feitas = False
                erros = []

                for p in self.__todos_participantes:
                    marcado_agora = valores[f"-P_{p.get_id()}-"]
                    estava_marcado = p.get_id() in self.__ids_no_evento

                    if marcado_agora and not estava_marcado:
                        sucesso, msg = self.__participacao_controller.adicionar_participante_evento(self.__evento.get_id(), p.get_id())
                        if sucesso:
                            alteracoes_feitas = True
                        else:
                            erros.append(f"Erro ao adicionar {p.get_username()}: {msg}")

                    elif not marcado_agora and estava_marcado:
                        sucesso, msg = self.__participacao_controller.remover_participante_evento(self.__evento.get_id(), p.get_id())
                        if sucesso:
                            alteracoes_feitas = True
                        else:
                            erros.append(f"Erro ao remover {p.get_username()}: {msg}")

                if erros:
                    sg.popup_error("\n".join(erros))
                elif alteracoes_feitas:
                    sg.popup("Participantes atualizados com sucesso!")
                    self.fechar()
                    return "menu_eventos", self.__organizador, None
                else:
                    sg.popup("Nenhuma alteração realizada.")

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None