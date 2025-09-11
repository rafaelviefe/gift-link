from typing import Optional

class Usuario:
    def __init__(self, username: str, senha: str, id: Optional[int] = None):
        self.__id = id
        self.__username = username
        self.__senha = senha

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_username(self) -> str:
        return self.__username

    def get_senha(self) -> str:
        return self.__senha

    def set_id(self, id: int) -> None:
        self.__id = id

    def set_username(self, username: str) -> None:
        self.__username = username

    def set_senha(self, senha: str) -> None:
        self.__senha = senha
