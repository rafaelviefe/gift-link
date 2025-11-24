import FreeSimpleGUI as sg

from controller.sorteio_controller import SorteioController
from model.participante import Participante
from views.theme import configure_theme


class TelaMeusSorteios:
    def __init__(self, participante: Participante):
        configure_theme()
        self.__participante = participante
        self.__sorteio_controller = SorteioController()
        self.__janela = None
        self.__dados_sorteios = []

    def __criar_janela(self):
        # Busca os dados no controller
        self.__dados_sorteios, msg = self.__sorteio_controller.listar_meus_sorteios(self.__participante)

        # Formata para exibir na lista (Apenas Nome do Evento e Status)
        lista_exibicao = []
        for item in self.__dados_sorteios:
            lista_exibicao.append(f"{item['evento']} ({item['status']})")

        layout = [
            [sg.Text("Meus Amigos Secretos", font=("Helvetica", 20, "bold"))],
            [sg.Text("Selecione um evento para ver quem você tirou:")],
            [
                sg.Listbox(
                    values=lista_exibicao,
                    size=(50, 6),
                    key="-LISTA_EVENTOS-",
                    enable_events=True,
                    font=("Helvetica", 12)
                )
            ],
            [sg.VPush()],
            [sg.Text("", size=(40, 2), key="-RESULTADO-", font=("Helvetica", 14, "bold"), justification='center', text_color="#2ecc71")],
            [sg.VPush()],
            [sg.Button("Ver Quem Eu Tirei", key="-VER-", disabled=True), sg.Button("Voltar", key="-VOLTAR-")]
        ]

        return sg.Window(
            "Meus Eventos - GiftLink",
            layout,
            finalize=True,
            element_justification="center",
            size=(500, 400)
        )

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == "-VOLTAR-":
                self.fechar()
                return "painel_participante", self.__participante, None

            # Habilita o botão apenas se algo estiver selecionado
            if evento == "-LISTA_EVENTOS-" and valores["-LISTA_EVENTOS-"]:
                self.__janela["-VER-"].update(disabled=False)
                # Limpa o resultado anterior para não confundir
                self.__janela["-RESULTADO-"].update("")

            if evento == "-VER-":
                selecao = valores["-LISTA_EVENTOS-"]
                if selecao:
                    # Descobre o índice selecionado para pegar o amigo secreto correspondente
                    index = self.__janela["-LISTA_EVENTOS-"].get_indexes()[0]
                    dados = self.__dados_sorteios[index]

                    amigo = dados["amigo_secreto"]
                    nome_evento = dados["evento"]

                    self.__janela["-RESULTADO-"].update(f"No evento '{nome_evento}':\nVocê tirou: {amigo}")

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None
