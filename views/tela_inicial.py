import FreeSimpleGUI as sg
from views.theme import configure_theme

class TelaInicial:
    def __init__(self):
        configure_theme()
        self.__janela = None

    def __criar_janela(self):
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

    def abrir(self):
        self.__janela = self.__criar_janela()
        
        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED:
                self.fechar()
                return "sair", None, None
            
            if evento == '-CADASTRO-':
                self.fechar()
                return "cadastro", None, None
            
            if evento == '-LOGIN-':
                self.fechar()
                return "login", None, None
    
    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None