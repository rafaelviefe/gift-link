from ast import Tuple
import hashlib
import secrets
import string

def criptografar_senha(senha: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(senha.encode('utf-8'))
    return sha256.hexdigest()

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return criptografar_senha(senha) == hash_senha

def criar_senha_provisoria() -> tuple[str, str]:
    chars = string.ascii_letters + string.digits
    senha = ''.join(secrets.choice(chars) for _ in range(6))
    return senha, criptografar_senha(senha)

def valida_entrada(username: str, senha: str) -> bool:
    return username == "" or len(senha) < 6