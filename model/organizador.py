from typing import Optional
from model.usuario import Usuario

class Organizador(Usuario):
    def __init__(self, username: str, senha: str, id: Optional[int] = None):
        super().__init__(username, senha, id)
