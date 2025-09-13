import FreeSimpleGUI as sg
from typing import Optional
from controller.organizador_controller import OrganizadorController
from controller.participante_controller import ParticipanteController
from model.organizador import Organizador
from model.participante import Participante
from views.tela_inicial import TelaInicial
from views.tela_login import TelaLogin
from views.tela_cadastro_organizador import TelaCadastroOrganizador
from views.tela_organizador import TelaOrganizador
from views.tela_participante import TelaParticipante
from views.tela_alterar_senha import TelaAlterarSenha
from views.tela_cadastro_participante import TelaCadastroParticipante

class App:
    def __init__(self):
        self.__organizador_controller = OrganizadorController()
        self.__participante_controller = ParticipanteController()
        self.__organizador_logado: Optional[Organizador] = None
        self.__participante_logado: Optional[Participante] = None

    def run(self):
        tela_atual = TelaInicial()

        while tela_atual is not None:
            proxima_tela_str, evento, valores = tela_atual.abrir()

            if proxima_tela_str == "sair":
                break

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

            elif isinstance(tela_atual, (TelaOrganizador, TelaParticipante)):
                if proxima_tela_str == "logout":
                    self.__organizador_logado = None
                    self.__participante_logado = None
                    tela_atual = TelaInicial()
                elif proxima_tela_str == "gerenciar_participantes":
                     tela_atual = TelaCadastroParticipante(self.__participante_controller, self.__organizador_logado)
            
            elif isinstance(tela_atual, TelaCadastroParticipante):
                if proxima_tela_str == "painel_organizador":
                    tela_atual = TelaOrganizador(self.__organizador_logado)

        if hasattr(tela_atual, 'fechar'):
            tela_atual.fechar()
