from typing import Optional

class Usuario:
    def __init__(self, username: str, senha: str, id: Optional[int] = None):
        self._id = id
        self._username = username
        self._senha = senha

    def get_id(self) -> Optional[int]:
        return self._id

    def get_username(self) -> str:
        return self._username

    def get_senha(self) -> str:
        return self._senha

    def set_id(self, id: int) -> None:
        self._id = id

    def set_username(self, username: str) -> None:
        self._username = username

    def set_senha(self, senha: str) -> None:
        self._senha = senha
