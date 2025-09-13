from typing import Tuple, Optional
from model.organizador import Organizador
from model.chave import Chave
from repository import organizador_repository, chave_repository
from utils.seguranca import criptografar_senha, verificar_senha, valida_entrada

def registrar_organizador(username: str, senha: str, chave_acesso_id: str) -> Tuple[Optional[Organizador], str]:
    if not valida_entrada(username, senha):
        return (None, "Usuário ou senha inválidos.")
    
    chave_para_verificar = Chave(id=chave_acesso_id)
    chave_valida, msg_chave = chave_repository.verificar_chave(chave_para_verificar)

    if not chave_valida:
        return (None, msg_chave)

    senha_criptografada = criptografar_senha(senha)
    novo_organizador = Organizador(username=username, senha=senha_criptografada)
    
    return organizador_repository.criar_organizador(novo_organizador)

def login_organizador(username: str, senha: str) -> Tuple[Optional[Organizador], str]:
    if not valida_entrada(username, senha):
        return (None, "Usuário ou senha inválidos.")
    
    organizador_encontrado, msg_busca = organizador_repository.buscar_organizador(username)

    if not organizador_encontrado:
        return (None, msg_busca)

    senha_salva: str = organizador_encontrado.get_senha()
    
    if verificar_senha(senha, senha_salva):
        return (organizador_encontrado, "Login realizado com sucesso!")
    else:
        return (None, "Senha incorreta.")