import FreeSimpleGUI as sg
from views.theme import configure_theme
from controller.organizador_controller import OrganizadorController
from controller.participante_controller import ParticipanteController

class TelaLogin:
    def __init__(self, organizador_controller: OrganizadorController, participante_controller: ParticipanteController):
        configure_theme()
        self.__organizador_controller = organizador_controller
        self.__participante_controller = participante_controller
        self.__janela = None

    def __criar_janela(self):
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

    def abrir(self):
        self.__janela = self.__criar_janela()

        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == '-VOLTAR-':
                self.fechar()
                return "inicio", None, None

            if evento == '-SUBMIT-':
                username = valores["-USERNAME-"]
                senha = valores["-SENHA-"]

                if valores['-ORGANIZADOR-']:
                    organizador, mensagem = self.__organizador_controller.login(username, senha)
                    if organizador:
                        sg.popup_ok(mensagem)
                        self.fechar()
                        return "login_organizador_sucesso", organizador, None
                    else:
                        sg.popup_error(mensagem)
                else:
                    participante, mensagem = self.__participante_controller.login(username, senha)
                    if participante:
                        if not participante.is_elegivel():
                            sg.popup("Você precisa alterar sua senha para continuar.")
                            self.fechar()
                            return "alterar_senha", participante, None
                        else:
                            sg.popup_ok(mensagem)
                            self.fechar()
                            return "login_participante_sucesso", participante, None
                    else:
                        sg.popup_error(mensagem)

    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None