import FreeSimpleGUI as sg
from views.theme import configure_theme
from model.participante import Participante

def criar_janela_participante(participante: Participante):
    configure_theme()

    layout = [
        [
            sg.Text(
                f"Bem-vindo, {participante.get_username()}!",
                font=("Helvetica", 20, "bold"),
            )
        ],
        [sg.VPush()],
        [sg.Button("Visualizar Eventos", key="-MEUSEVENTOS-")],
        [sg.Button("Lista de Desejos", key="-DESEJOS-")],
        [sg.Button("Logout", key="-LOGOUT-")],
        [sg.VPush()],
    ]

    return sg.Window(
        f"Painel do Participante - {participante.get_username()}",
        layout,
        finalize=True,
        element_justification="center",
        size=(500, 400),
    )