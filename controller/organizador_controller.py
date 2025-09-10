from typing import Tuple, Optional
from model.organizador import Organizador
from model.chave import Chave
from repository import organizador_repository, chave_repository
from utils.seguranca import criptografar_senha

def registrar_organizador(username: str, senha: str, chave_acesso_id: str) -> Tuple[Optional[Organizador], str]:
    chave_para_verificar = Chave(id=chave_acesso_id)
    chave_valida, msg_chave = chave_repository.verificar_chave(chave_para_verificar)

    if not chave_valida:
        return (None, msg_chave)

    senha_criptografada = criptografar_senha(senha)
    novo_organizador = Organizador(username=username, senha=senha_criptografada)
    
    return organizador_repository.criar_organizador(novo_organizador)