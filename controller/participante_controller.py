from typing import Tuple, Optional
from model.participante import Participante
from repository import participante_repository
from utils.seguranca import criar_senha_provisoria, verificar_senha, valida_entrada


def registrar_participante(username: str) -> Tuple[Optional[Participante], str]:
    senha_crua, hash_senha = criar_senha_provisoria()

    if not valida_entrada(username, senha_crua):
        return (None, "Usuário ou senha inválidos.")

    novo_participante = Participante(username=username, senha=hash_senha)

    participante, mensagem = participante_repository.criar_participante(
        novo_participante
    )
    if not participante:
        return None, mensagem
    return (
        participante,
        f"Participante {participante.get_username()} criado com sucesso! A senha provisória é: {senha_crua}",
    )

def listar_participantes() -> Tuple[list[Participante], str]:
    participantes, mensagem = participante_repository.listar_participantes()
    if participantes == []:
        return [], mensagem
    return participantes, mensagem

def login_participante(username: str, senha: str) -> Tuple[Optional[Participante], str]:
    if not valida_entrada(username, senha):
        return (None, "Usuário ou senha inválidos.")
    
    participante_encontrado, msg_busca = participante_repository.buscar_participante(username)

    if not participante_encontrado:
        return (None, msg_busca)

    senha_salva: str = participante_encontrado.get_senha()
    
    if verificar_senha(senha, senha_salva):
        return (participante_encontrado, "Login realizado com sucesso!")
    else:
        return (None, "Senha incorreta.")
    

