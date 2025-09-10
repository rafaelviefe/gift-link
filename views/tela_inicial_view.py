import PySimpleGUI as sg
from views.theme import configure_theme

def criar_janela_inicial():
    configure_theme()

    layout = [
        [sg.Text('GiftLink', font=('Helvetica', 28, 'bold'), justification='center', expand_x=True)],
        [sg.Text('Sua ferramenta para amigo secreto', font=('Helvetica', 14), justification='center', expand_x=True)],
        [sg.VPush()],
        [sg.Button('Fazer Cadastro', key='-CADASTRO-')],
        [sg.Button('Login', key='-LOGIN-')],
        [sg.VPush()],
    ]

    return sg.Window(
        'Bem-vindo ao GiftLink',
        layout,
        finalize=True,
        element_justification='center',
        size=(400, 300)
    )