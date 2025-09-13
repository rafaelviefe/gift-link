import FreeSimpleGUI as sg
from views.theme import configure_theme
from controller.participante_controller import ParticipanteController
from model.participante import Participante

class TelaAlterarSenha:
    def __init__(self, participante_controller: ParticipanteController, participante_pendente: Participante):
        configure_theme()
        self.__participante_controller = participante_controller
        self.__participante_pendente = participante_pendente
        self.__janela = None

    def __criar_janela(self):
        username = self.__participante_pendente.get_username()
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

    def abrir(self):
        self.__janela = self.__criar_janela()
        
        while True:
            evento, valores = self.__janela.read()

            if evento == sg.WIN_CLOSED or evento == '-CANCELAR-':
                self.fechar()
                return "inicio", None, None

            if evento == '-CONFIRMAR-':
                nova_senha = valores["-NOVA_SENHA-"]
                username = self.__participante_pendente.get_username()
                
                sucesso, mensagem = self.__participante_controller.alterar_senha(username, nova_senha)
                
                if sucesso:
                    sg.popup_ok(mensagem)
                    self.fechar()
                    return "login_participante_sucesso", self.__participante_pendente, None
                else:
                    sg.popup_error(mensagem)
    
    def fechar(self):
        if self.__janela:
            self.__janela.close()
            self.__janela = None