import FreeSimpleGUI as sg
from views import (
    tela_inicial_view,
    tela_cadastro_view,
    tela_organizador_view,
    tela_cadastro_participante_view,
)
from controller import organizador_controller, participante_controller
from model.organizador import Organizador
from typing import Optional


def main():
    organizador_logado: Optional[Organizador] = None

    janela_inicial = tela_inicial_view.criar_janela_inicial()
    janela_cadastro, janela_organizador, janela_cadastro_participante = None, None, None

    while True:
        janela_ativa, evento, valores = sg.read_all_windows()

        if evento == sg.WIN_CLOSED:
            break

        if janela_ativa == janela_inicial:
            if evento == "-CADASTRO-":
                janela_inicial.hide()
                janela_cadastro = tela_cadastro_view.criar_janela_cadastro()
            elif evento == "-LOGIN-":
                sg.popup("Funcionalidade de Login será implementada em breve!")

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

                    janela_organizador = tela_organizador_view.criar_janela_organizador(
                        organizador_logado
                    )
                else:
                    sg.popup_error(mensagem)

        elif janela_ativa == janela_organizador:
            if evento == "-LOGOUT-":
                organizador_logado = None

                janela_organizador.close()
                janela_organizador = None

                janela_inicial = tela_inicial_view.criar_janela_inicial()
            elif evento == "-PARTICIPANTES-":
                janela_organizador.hide()
                # fetch participantes and open cadastro window with current list
                participantes, _msg = participante_controller.listar_participantes()
                janela_cadastro_participante = (
                    tela_cadastro_participante_view.criar_janela_cadastro(participantes)
                )
            elif evento == "-SORTEIOS-":
                sg.popup(
                    f"Funcionalidade de '{evento.strip('-')}' será implementada em breve!"
                )

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
                # refresh table with latest participantes from repository
                participantes, _msg = participante_controller.listar_participantes()
                tela_cadastro_participante_view.atualizar_tabela(
                    janela_cadastro_participante, participantes
                )
                # clear input
                try:
                    janela_cadastro_participante["-USERNAME-"].update("")
                except Exception:
                    pass

    if janela_inicial:
        janela_inicial.close()
    if janela_cadastro:
        janela_cadastro.close()
    if janela_organizador:
        janela_organizador.close()
    if janela_cadastro_participante:
        janela_cadastro_participante.close()


if __name__ == "__main__":
    main()
