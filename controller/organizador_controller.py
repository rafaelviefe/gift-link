from typing import Tuple, Optional
from model.organizador import Organizador
from model.chave import Chave
from repository.organizador_repository import OrganizadorRepository
from repository.chave_repository import ChaveRepository
from utils.seguranca import Seguranca

class OrganizadorController:
    def __init__(self):
        self.__organizador_repository = OrganizadorRepository()
        self.__chave_repository = ChaveRepository()
        self.__seguranca = Seguranca()

    def registrar(self, username: str, senha: str, chave_acesso_id: str) -> Tuple[Optional[Organizador], str]:

        credenciais_validas = self.__seguranca.valida_credenciais(username, senha)
        if not credenciais_validas:
            return (None, "Usuário ou senha inválidos.")
        
        chave_para_verificar = Chave(id=chave_acesso_id)
        chave_valida, msg_chave = self.__chave_repository.verificar(chave_para_verificar)

        if not chave_valida:
            return (None, msg_chave)

        senha_criptografada = self.__seguranca.criptografar_senha(senha)
        novo_organizador = Organizador(username=username, senha=senha_criptografada)
        
        return self.__organizador_repository.criar(novo_organizador)

    def login(self, username: str, senha: str) -> Tuple[Optional[Organizador], str]:
        credenciais_validas = self.__seguranca.valida_credenciais(username, senha)
        if not credenciais_validas:
            return (None, "Usuário ou senha inválidos.")
        
        organizador_encontrado, msg_busca = self.__organizador_repository.buscar(username)

        if not organizador_encontrado:
            return (None, msg_busca)

        senha_salva: str = organizador_encontrado.get_senha()
        
        senha_correta = self.__seguranca.verificar_senha(senha, senha_salva)
        if senha_correta:
            return (organizador_encontrado, "Login realizado com sucesso!")
        else:
            return (None, "Senha incorreta.")