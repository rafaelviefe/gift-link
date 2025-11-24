import FreeSimpleGUI as sg

from controller.sorteio_controller import SorteioController
from model.evento import Evento
from model.organizador import Organizador
from views.theme import configure_theme


class TelaVisualizarSorteioGeral:
    def __init__(self, evento: Evento, organizador: Organizador):
        configure_theme()
        self.__evento = evento
        self.__organizador = organizador
        self.__sorteio_controller = SorteioController()
        self.__janela = None

    def __criar_janela(self):
        dados, _ = self.__sorteio_controller.ver_mapeamento_geral(self.__evento)

        # Formata para tabela
        tabela_valores = []
        for linha in dados:
            tabela_valores.append([linha['quem_tirou'], "-->", linha['quem_foi_tirado']])

        layout = [
            [sg.Text(f"Resultado: {self.__evento.get_nome()}", font=("Helvetica", 18, "bold"))],
            [sg.Text("Atenção: Você está vendo todos os pares gerados.", text_color="yellow")],
            [
                sg.Table(
                    values=tabela_valores,
                    headings=["Participante (Origem)", "  ", "Amigo Secreto (Destino)"],
                    auto_size_columns=False,
                    col_widths=[25, 5, 25],
                    justification="center",
                    num_rows=15,
                    key="-TABLE-"
                )
            ],
            [sg.Button("Voltar", key="-VOLTAR-")]
        ]

        return sg.Window("Mapeamento do Sorteio - GiftLink", layout, finalize=True, element_justification="center")

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evt, valores = self.__janela.read()

            if evt == sg.WIN_CLOSED or evt == "-VOLTAR-":
                self.fechar()
                # Retorna para a lista de sorteios
                return "menu_sorteios", self.__organizador, None

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None
