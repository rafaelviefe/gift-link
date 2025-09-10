import hashlib

def criptografar_senha(senha: str) -> str:
    sha256 = hashlib.sha256()
    sha256.update(senha.encode('utf-8'))
    return sha256.hexdigest()

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return criptografar_senha(senha) == hash_senha