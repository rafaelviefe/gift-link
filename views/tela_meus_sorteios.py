import FreeSimpleGUI as sg

from controller.participacao_controller import ParticipacaoController
from controller.sorteio_controller import SorteioController
from model.participante import Participante
from model.status_evento import StatusEvento
from views.theme import configure_theme


class TelaMeusSorteios:
    def __init__(self, participante: Participante):
        configure_theme()
        self.__participante = participante
        self.__participacao_controller = ParticipacaoController()
        self.__sorteio_controller = SorteioController()
        self.__janela = None
        self.__participacoes = []

    def __criar_janela(self):
        # Busca TODAS as participações (eventos sorteados ou não)
        self.__participacoes, msg = self.__participacao_controller.listar_eventos_do_participante(self.__participante)

        lista_exibicao = []
        if self.__participacoes:
            for p in self.__participacoes:
                evento = p.get_evento()
                lista_exibicao.append(f"{evento.get_id()} - {evento.get_nome()} ({evento.get_status().value})")
        else:
            lista_exibicao.append("Nenhuma participação encontrada.")

        layout = [
            [sg.Text("Meus Eventos", font=("Helvetica", 20, "bold"))],
            [sg.Text("Selecione um evento para ver detalhes:", font=("Helvetica", 11))],
            [
                sg.Listbox(
                    values=lista_exibicao,
                    size=(50, 8),
                    key="-LISTA_EVENTOS-",
                    enable_events=True,
                    font=("Helvetica", 12)
                )
            ],
            [sg.VPush()],
            [sg.Text("", size=(45, 3), key="-RESULTADO-", font=("Helvetica", 12, "bold"), justification='center', text_color="#2ecc71")],
            [sg.VPush()],
            [sg.Button("Ver Amigo Secreto", key="-VER-", disabled=True), sg.Button("Voltar", key="-VOLTAR-")]
        ]

        return sg.Window(
            "Meus Eventos - GiftLink",
            layout,
            finalize=True,
            element_justification="center",
            size=(500, 450)
        )

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == "-VOLTAR-":
                self.fechar()
                return "painel_participante", self.__participante, None

            if evento == "-LISTA_EVENTOS-" and valores["-LISTA_EVENTOS-"]:
                selecao = valores["-LISTA_EVENTOS-"][0]
                
                if selecao == "Nenhuma participação encontrada.":
                    self.__janela["-VER-"].update(disabled=True)
                    self.__janela["-RESULTADO-"].update("")
                    continue

                # Recupera o objeto Participacao baseado no índice da lista
                index = self.__janela["-LISTA_EVENTOS-"].get_indexes()[0]
                if index < len(self.__participacoes):
                    participacao_selecionada = self.__participacoes[index]
                    evento_obj = participacao_selecionada.get_evento()
                    
                    # Lógica de Estado
                    if evento_obj.get_status() == StatusEvento.PREPARANDO:
                        self.__janela["-VER-"].update(disabled=True)
                        self.__janela["-RESULTADO-"].update("⏳ Aguardando Sorteio...\nO organizador ainda não realizou o sorteio.", text_color="orange")
                    else:
                        # Sorteado ou Finalizado
                        self.__janela["-VER-"].update(disabled=False)
                        self.__janela["-RESULTADO-"].update("🎁 Sorteio Realizado!\nClique no botão abaixo para ver quem você tirou.", text_color="green")

            if evento == "-VER-":
                if valores["-LISTA_EVENTOS-"]:
                    index = self.__janela["-LISTA_EVENTOS-"].get_indexes()[0]
                    evento_obj = self.__participacoes[index].get_evento()
                    
                    msg_resultado = self.__sorteio_controller.verificar_quem_tirei(
                        evento_obj.get_id(), 
                        self.__participante.get_id()
                    )
                    self.__janela["-RESULTADO-"].update(msg_resultado, text_color="#2ecc71")

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None