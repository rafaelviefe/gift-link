import FreeSimpleGUI as sg
from views.theme import configure_theme
from controller.organizador_controller import OrganizadorController

class TelaCadastroOrganizador:
    def __init__(self, organizador_controller: OrganizadorController):
        configure_theme()
        self.__organizador_controller = organizador_controller
        self.__janela = None

    def __criar_janela(self):
        layout = [
            [sg.Text('Cadastro de Organizador', font=('Helvetica', 20, 'bold'))],
            [sg.Text('Username', size=(15, 1)), sg.InputText(key='-USERNAME-')],
            [sg.Text('Senha', size=(15, 1)), sg.InputText(key='-SENHA-', password_char='*')],
            [sg.Text('Código de Acesso', size=(15, 1)), sg.InputText(key='-CHAVE-')],
            [sg.Button('Cadastrar', key='-SUBMIT-'), sg.Button('Voltar', key='-VOLTAR-')]
        ]
        return sg.Window(
            'Cadastro - GiftLink',
            layout,
            finalize=True,
            element_justification='center'
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
                chave = valores["-CHAVE-"]

                organizador, msg = self.__organizador_controller.registrar_organizador(username, senha, chave)

                if organizador:
                    sg.popup_ok(msg)
                    self.fechar()
                    return "login_organizador_sucesso", organizador, None
                else:
                    sg.popup_error(msg)
    
    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None