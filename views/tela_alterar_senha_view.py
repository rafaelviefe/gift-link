import FreeSimpleGUI as sg
from views.theme import configure_theme

def criar_janela_alterar_senha(username: str):
    configure_theme()

    layout = [
        [sg.Text('Alterar Senha', font=('Helvetica', 28, 'bold'), justification='center', expand_x=True)],
        [sg.Text(f"Usuário: {username}", font=('Helvetica', 14))],
        [sg.Text('Nova Senha', size=(15, 1)), sg.InputText(key='-NOVA_SENHA-', password_char='*')],
        [sg.VPush()],
        [sg.Button('Confirmar', key='-CONFIRMAR-'), sg.Button('Cancelar', key='-CANCELAR-')],
        [sg.VPush()],
    ]

    return sg.Window(
        'Alterar Senha - GiftLink',
        layout,
        finalize=True,
        element_justification='center',
        size=(400, 250)
    )