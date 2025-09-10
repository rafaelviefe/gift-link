from typing import Optional
from model.usuario import Usuario

class Participante(Usuario):
    def __init__(self, username: str, senha: str, id: Optional[int] = None, elegivel: bool = True):
        super().__init__(username, senha, id)
        self._elegivel = elegivel

    def is_elegivel(self) -> bool:
        return self._elegivel

    def set_elegivel(self, elegivel: bool) -> None:
        self._elegivel = elegivel
