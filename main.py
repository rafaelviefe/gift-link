import FreeSimpleGUI as sg
from views import (
    tela_alterar_senha,
    tela_cadastro,
    tela_cadastro_participante,
    tela_inicial,
    tela_login,
    tela_organizador,
    tela_participante
)
from controller import organizador_controller, participante_controller
from model.organizador import Organizador
from model.participante import Participante
from typing import Optional

def main():
    organizador_logado: Optional[Organizador] = None
    participante_logado: Optional[Participante] = None
    participante_pendente: Optional[Participante] = None

    janela_inicial = tela_inicial.criar_janela_inicial()
    janela_cadastro, janela_login, janela_organizador, janela_participante, janela_cadastro_participante, janela_alterar_senha = None, None, None, None, None, None

    while True:
        janela_ativa, evento, valores = sg.read_all_windows()

        if evento == sg.WIN_CLOSED:
            break

        if janela_ativa == janela_inicial:
            if evento == "-CADASTRO-":
                janela_inicial.hide()
                janela_cadastro = tela_cadastro.criar_janela_cadastro()
            elif evento == "-LOGIN-":
                janela_inicial.hide()
                janela_login = tela_login.criar_janela_login()

        elif janela_ativa == janela_cadastro:
            if evento == "-VOLTAR-":
                janela_cadastro.close()
                janela_cadastro = None
                janela_inicial.un_hide()
            elif evento == "-SUBMIT-":
                username = valores["-USERNAME-"]
                senha = valores["-SENHA-"]
                chave = valores["-CHAVE-"]

                organizador, mensagem = organizador_controller.registrar_organizador(
                    username, senha, chave
                )

                if organizador:
                    sg.popup_ok(mensagem)
                    organizador_logado = organizador
                    janela_cadastro.close()
                    janela_cadastro = None
                    janela_inicial.close()
                    janela_organizador = tela_organizador.criar_janela_organizador(
                        organizador_logado
                    )
                else:
                    sg.popup_error(mensagem)

        elif janela_ativa == janela_login:
            if evento == "-VOLTAR-":
                janela_login.close()
                janela_login = None
                janela_inicial.un_hide()
            elif evento == "-SUBMIT-":
                username = valores["-USERNAME-"]
                senha = valores["-SENHA-"]

                if valores['-ORGANIZADOR-']:
                    organizador, mensagem = organizador_controller.login_organizador(username, senha)
                    if organizador:
                        sg.popup_ok(mensagem)
                        organizador_logado = organizador
                        janela_login.close()
                        janela_login = None
                        janela_inicial.close()
                        janela_organizador = tela_organizador.criar_janela_organizador(organizador_logado)
                    else:
                        sg.popup_error(mensagem)
                else:
                    participante, mensagem = participante_controller.login_participante(username, senha)
                    if participante:
                        if not participante.is_elegivel():
                            sg.popup("Você precisa alterar sua senha para continuar.")
                            participante_pendente = participante
                            janela_alterar_senha = tela_alterar_senha.criar_janela_alterar_senha(participante.get_username())
                            janela_login.hide()
                        else:
                            sg.popup_ok(mensagem)
                            participante_logado = participante
                            janela_login.close()
                            janela_login = None
                            janela_inicial.close()
                            janela_participante = tela_participante.criar_janela_participante(participante_logado)
                    else:
                        sg.popup_error(mensagem)

        elif janela_ativa == janela_alterar_senha:
            if evento == "-CANCELAR-":
                janela_alterar_senha.close()
                janela_alterar_senha = None
                participante_pendente = None
                janela_login.un_hide()
            elif evento == "-CONFIRMAR-":
                nova_senha = valores["-NOVA_SENHA-"]
                if participante_pendente:
                    username_participante = participante_pendente.get_username()
                    sucesso, mensagem = participante_controller.alterar_senha(username_participante, nova_senha)
                    if sucesso:
                        sg.popup_ok(mensagem)
                        participante_logado = participante_pendente
                        participante_pendente = None
                        
                        janela_alterar_senha.close()
                        janela_alterar_senha = None
                        janela_login.close()
                        janela_login = None
                        janela_inicial.close()
                        
                        janela_participante = tela_participante.criar_janela_participante(participante_logado)
                    else:
                        sg.popup_error(mensagem)

        elif janela_ativa == janela_organizador:
            if evento == "-LOGOUT-":
                organizador_logado = None
                janela_organizador.close()
                janela_organizador = None
                janela_inicial = tela_inicial.criar_janela_inicial()
            elif evento == "-PARTICIPANTES-":
                janela_organizador.hide()
                participantes, _msg = participante_controller.listar_participantes()
                janela_cadastro_participante = (
                    tela_cadastro_participante.criar_janela_cadastro(participantes)
                )
            elif evento == "-EVENTOS-":
                sg.popup(
                    f"Funcionalidade de '{evento.strip('-')}' será implementada em breve!"
                )

        elif janela_ativa == janela_participante:
            if evento == "-LOGOUT-":
                participante_logado = None
                janela_participante.close()
                janela_participante = None
                janela_inicial = tela_inicial.criar_janela_inicial()
            elif evento in ["-MEUSEVENTOS-", "-DESEJOS-"]:
                sg.popup(f"Funcionalidade de '{evento.strip('-')}' será implementada em breve!")

        elif janela_ativa == janela_cadastro_participante:
            if evento == "-VOLTAR-":
                janela_cadastro_participante.close()
                janela_cadastro_participante = None
                janela_organizador.un_hide()
            elif evento == "-SUBMIT-":
                username = valores["-USERNAME-"]
                participante, mensagem = participante_controller.registrar_participante(
                    username
                )
                sg.popup(mensagem)
                participantes, _msg = participante_controller.listar_participantes()
                tela_cadastro_participante.atualizar_tabela(
                    janela_cadastro_participante, participantes
                )
                try:
                    janela_cadastro_participante["-USERNAME-"].update("")
                except Exception:
                    pass

    if janela_inicial:
        janela_inicial.close()
    if janela_cadastro:
        janela_cadastro.close()
    if janela_login:
        janela_login.close()
    if janela_organizador:
        janela_organizador.close()
    if janela_participante:
        janela_participante.close()
    if janela_cadastro_participante:
        janela_cadastro_participante.close()
    if janela_alterar_senha:
        janela_alterar_senha.close()

if __name__ == "__main__":
    main()