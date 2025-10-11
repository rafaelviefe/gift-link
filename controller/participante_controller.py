from typing import Tuple, Optional, List
from model.participante import Participante
from repository.participante_repository import ParticipanteRepository
from utils.seguranca import (
    criar_senha_provisoria,
    verificar_senha,
    valida_credenciais,
    criptografar_senha,
    valida_usuario,
)

class ParticipanteController:
    def __init__(self):
        self.__participante_repository = ParticipanteRepository()

    def registrar_participante(self, username: str) -> Tuple[Optional[Participante], str]:
        if not valida_usuario(username):
            return (None, "Usuário inválido")

        participante_existente, _ = self.__participante_repository.buscar_participante(username)
        if participante_existente:
            return (None, "Nome de usuário já existe")

        senha_crua, hash_senha = criar_senha_provisoria()
        novo_participante = Participante(username=username, senha=hash_senha)

        participante_criado, mensagem = self.__participante_repository.criar_participante(
            novo_participante
        )
        if not participante_criado:
            return None, mensagem

        return (
            participante_criado,
            f"Participante {participante_criado.get_username()} criado com sucesso! A senha provisória é: {senha_crua}",
        )

    def listar_participantes(self) -> Tuple[List[Participante], str]:
        participantes, mensagem = self.__participante_repository.listar_participantes()
        return participantes, mensagem

    def login_participante(self, username: str, senha: str) -> Tuple[Optional[Participante], str]:
        if not valida_credenciais(username, senha):
            return (None, "Usuário ou senha inválidos.")
        
        participante_encontrado, msg_busca = self.__participante_repository.buscar_participante(username)

        if not participante_encontrado:
            return (None, msg_busca)

        senha_salva: str = participante_encontrado.get_senha()
        
        if verificar_senha(senha, senha_salva):
            return (participante_encontrado, "Login realizado com sucesso!")
        else:
            return (None, "Senha incorreta.")
    
    def alterar_senha(self, username: str, nova_senha: str) -> Tuple[bool, str]:
        if not valida_credenciais(username, nova_senha):
            return (False, "A nova senha fornecida é inválida.")

        participante_encontrado, msg_busca = self.__participante_repository.buscar_participante(username)
        if not participante_encontrado:
            return (False, msg_busca)
        
        hash_nova_senha = criptografar_senha(nova_senha)

        return self.__participante_repository.alterar_senha_participante(username, hash_nova_senha)