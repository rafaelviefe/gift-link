from typing import Tuple, Optional
from model.participante import Participante
from repository import participante_repository
from utils.seguranca import criar_senha_provisoria


def registrar_participante(username: str) -> Tuple[Optional[Participante], str]:
    if username == "":
        return None, "Username do participante deve ser fornecido."

    senha_crua, hash_senha = criar_senha_provisoria()
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
