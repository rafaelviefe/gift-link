from typing import Optional

import FreeSimpleGUI as sg

from controller.evento_controller import EventoController
from controller.item_controller import ItemController
from controller.organizador_controller import OrganizadorController
from controller.participante_controller import ParticipanteController
from model.organizador import Organizador
from model.participante import Participante
from model.status_evento import StatusEvento

# Views de Autenticação e Cadastro
from views.tela_inicial import TelaInicial
from views.tela_login import TelaLogin
from views.tela_cadastro_organizador import TelaCadastroOrganizador
from views.tela_alterar_senha import TelaAlterarSenha

# Views do Organizador
from views.tela_organizador import TelaOrganizador
from views.tela_cadastro_participante import TelaCadastroParticipante
from views.tela_eventos_menu import TelaEventosMenu
from views.tela_cadastro_evento import TelaCadastroEvento
from views.tela_lista_sorteios_organizador import TelaListaSorteios
from views.tela_realizar_sorteio import TelaRealizarSorteio
from views.tela_vizualizar_mapeio_sorteio_organizador import TelaVisualizarSorteioGeral
from views.tela_selecionar_evento import TelaSelecionarEvento       
from views.tela_gerenciar_participacao import TelaGerenciarParticipacao 

# Views do Participante
from views.tela_participante import TelaParticipante
from views.tela_lista_desejos import TelaListaDesejos
from views.tela_meus_sorteios import TelaMeusSorteios


class App:
    def __init__(self):
        self.__organizador_controller = OrganizadorController()
        self.__participante_controller = ParticipanteController()
        self.__evento_controller = EventoController()
        self.__item_controller = ItemController()
        self.__organizador_logado: Optional[Organizador] = None
        self.__participante_logado: Optional[Participante] = None

    def run(self):
        tela_atual = TelaInicial()

        while tela_atual is not None:
            proxima_tela_str, evento, valores = tela_atual.abrir()

            if proxima_tela_str == "sair":
                break

            # --- Fluxo Inicial e Login ---
            if isinstance(tela_atual, TelaInicial):
                if proxima_tela_str == "login":
                    tela_atual = TelaLogin(self.__organizador_controller, self.__participante_controller)
                elif proxima_tela_str == "cadastro":
                    tela_atual = TelaCadastroOrganizador(self.__organizador_controller)

            elif isinstance(tela_atual, (TelaLogin, TelaCadastroOrganizador, TelaAlterarSenha)):
                 if proxima_tela_str == "inicio":
                    tela_atual = TelaInicial()
                 elif proxima_tela_str == "login_organizador_sucesso":
                    self.__organizador_logado = evento
                    tela_atual = TelaOrganizador(self.__organizador_logado)
                 elif proxima_tela_str == "login_participante_sucesso":
                    self.__participante_logado = evento
                    tela_atual = TelaParticipante(self.__participante_logado)
                 elif proxima_tela_str == "alterar_senha":
                    tela_atual = TelaAlterarSenha(self.__participante_controller, evento)

            # --- Fluxo do Organizador ---
            elif isinstance(tela_atual, TelaOrganizador):
                if proxima_tela_str == "logout":
                    self.__organizador_logado = None
                    self.__participante_logado = None
                    tela_atual = TelaInicial()
                elif proxima_tela_str == "gerenciar_participantes":
                     tela_atual = TelaCadastroParticipante(self.__participante_controller, self.__organizador_logado)
                elif proxima_tela_str == "gerenciar_eventos":
                     tela_atual = TelaEventosMenu(self.__organizador_logado)
                elif proxima_tela_str == "menu_sorteios":
                    tela_atual = TelaListaSorteios(self.__organizador_logado)

            elif isinstance(tela_atual, TelaCadastroParticipante):
                if proxima_tela_str == "painel_organizador":
                    tela_atual = TelaOrganizador(self.__organizador_logado)

            elif isinstance(tela_atual, TelaEventosMenu):
                if proxima_tela_str == "painel_organizador":
                    tela_atual = TelaOrganizador(self.__organizador_logado)
                elif proxima_tela_str == "cadastro_evento":
                    tela_atual = TelaCadastroEvento(self.__evento_controller, self.__organizador_logado)
                elif proxima_tela_str == "selecionar_evento_participacao":
                    tela_atual = TelaSelecionarEvento(self.__organizador_logado)

            elif isinstance(tela_atual, TelaCadastroEvento):
                 if proxima_tela_str == "menu_eventos":
                      tela_atual = TelaEventosMenu(self.__organizador_logado)

            elif isinstance(tela_atual, TelaSelecionarEvento):
                if proxima_tela_str == "voltar":
                    tela_atual = TelaEventosMenu(self.__organizador_logado)
                elif proxima_tela_str == "evento_selecionado":
                    tela_atual = TelaGerenciarParticipacao(evento, self.__organizador_logado)

            elif isinstance(tela_atual, TelaGerenciarParticipacao):
                if proxima_tela_str == "menu_eventos":
                    tela_atual = TelaEventosMenu(self.__organizador_logado)

            elif isinstance(tela_atual, TelaListaSorteios):
                if proxima_tela_str == "painel_organizador":
                    tela_atual = TelaOrganizador(self.__organizador_logado)

                elif proxima_tela_str == "acao_sorteio":
                    if evento.get_status() == StatusEvento.PREPARANDO:
                        tela_atual = TelaRealizarSorteio(evento, self.__organizador_logado)
                    else:
                        tela_atual = TelaVisualizarSorteioGeral(evento, self.__organizador_logado)

            elif isinstance(tela_atual, TelaVisualizarSorteioGeral):
                    if proxima_tela_str == "menu_sorteios":
                        tela_atual = TelaListaSorteios(self.__organizador_logado)

            elif isinstance(tela_atual, TelaRealizarSorteio):
                if proxima_tela_str == "menu_eventos":
                     tela_atual = TelaListaSorteios(self.__organizador_logado)

            # --- Fluxo do Participante ---
            elif isinstance(tela_atual, TelaParticipante):
                if proxima_tela_str == "logout":
                    self.__organizador_logado = None
                    self.__participante_logado = None
                    tela_atual = TelaInicial()
                elif proxima_tela_str == "lista_desejos":
                    tela_atual = TelaListaDesejos(self.__item_controller, self.__participante_logado)
                elif proxima_tela_str == "meus_sorteios":
                    tela_atual = TelaMeusSorteios(self.__participante_logado)

            elif isinstance(tela_atual, TelaListaDesejos):
                if proxima_tela_str == "painel_participante":
                    tela_atual = TelaParticipante(self.__participante_logado)

            elif isinstance(tela_atual, TelaMeusSorteios):
                if proxima_tela_str == "painel_participante":
                    tela_atual = TelaParticipante(self.__participante_logado)

        if hasattr(tela_atual, 'fechar'):
            tela_atual.fechar()