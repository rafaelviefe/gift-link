import FreeSimpleGUI as sg
from views.theme import configure_theme

def criar_janela_cadastro():
    configure_theme()

    layout = [
        [sg.Text('Cadastro de Participante', font=('Helvetica', 20, 'bold'))],
        [sg.Text('Username', size=(15, 1)), sg.InputText(key='-USERNAME-')],
        [sg.Button('Cadastrar', key='-SUBMIT-'), sg.Button('Voltar', key='-VOLTAR-')]
    ]

    return sg.Window(
        'Cadastro - GiftLink',
        layout,
        finalize=True,
        element_justification='center'
    )
