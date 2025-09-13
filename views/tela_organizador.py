import FreeSimpleGUI as sg
from views.theme import configure_theme
from model.organizador import Organizador


def criar_janela_organizador(organizador: Organizador):
    configure_theme()

    layout = [
        [
            sg.Text(
                f"Bem-vindo, {organizador.get_username()}!",
                font=("Helvetica", 20, "bold"),
            )
        ],
        [sg.VPush()],
        [sg.Button("Participantes", key="-PARTICIPANTES-")],
        [sg.Button("Eventos", key="-EVENTOS-")],
        [sg.Button("Logout", key="-LOGOUT-")],
        [sg.VPush()],
    ]

    return sg.Window(
        f"Painel do Organizador - {organizador.get_username()}",
        layout,
        finalize=True,
        element_justification="center",
        size=(500, 400),
    )
