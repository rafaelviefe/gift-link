import FreeSimpleGUI as sg
from views.theme import configure_theme

def criar_janela_login():
    configure_theme()

    layout = [
        [sg.Text('Login', font=('Helvetica', 28, 'bold'), justification='center', expand_x=True)],
        [sg.Text('Username', size=(15, 1)), sg.InputText(key='-USERNAME-')],
        [sg.Text('Senha', size=(15, 1)), sg.InputText(key='-SENHA-', password_char='*')],
        [sg.Radio('Organizador', "RADIO1", default=True, key='-ORGANIZADOR-'), 
         sg.Radio('Participante', "RADIO1", key='-PARTICIPANTE-')],
        [sg.VPush()],
        [sg.Button('Login', key='-SUBMIT-'), sg.Button('Voltar', key='-VOLTAR-')],
        [sg.VPush()],
    ]

    return sg.Window(
        'Login - GiftLink',
        layout,
        finalize=True,
        element_justification='center',
        size=(400, 300)
    )