from typing import Optional
from model.participante import Participante

class Item:
    def __init__(
        self,
        nome: str,
        preco: float,
        participante: Participante,
        id: Optional[int] = None,
    ):
        self.__id = id
        self.__nome = nome
        self.__preco = preco
        self.__participante = participante

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_preco(self) -> float:
        return self.__preco

    def get_participante(self) -> Participante:
        return self.__participante
    
    def get_id_participante(self) -> Optional[int]:
        return self.__participante.get_id()

    def set_id(self, id: int) -> None:
        self.__id = id

    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    def set_preco(self, preco: float) -> None:
        self.__preco = preco

    def set_participante(self, participante: Participante) -> None:
        self.__participante = participante