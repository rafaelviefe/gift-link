from typing import Optional
from model.organizador import Organizador
from model.status_evento import StatusEvento

class Evento:
    def __init__(
        self,
        nome: str,
        descricao: str,
        min_participantes: int,
        max_participantes: int,
        organizador: Organizador,
        status: StatusEvento = StatusEvento.PREPARANDO,
        id: Optional[int] = None,
    ):
        self.__id = id
        self.__nome = nome
        self.__descricao = descricao
        self.__min_participantes = min_participantes
        self.__max_participantes = max_participantes
        self.__status = status
        self.__organizador = organizador

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_nome(self) -> str:
        return self.__nome

    def get_descricao(self) -> str:
        return self.__descricao

    def get_min_participantes(self) -> int:
        return self.__min_participantes

    def get_max_participantes(self) -> int:
        return self.__max_participantes

    def get_status(self) -> StatusEvento:
        return self.__status

    def get_organizador(self) -> Organizador:
        return self.__organizador
    
    def get_id_organizador(self) -> Optional[int]:
        return self.__organizador.get_id()

    def set_id(self, id: int) -> None:
        self.__id = id

    def set_nome(self, nome: str) -> None:
        self.__nome = nome

    def set_descricao(self, descricao: str) -> None:
        self.__descricao = descricao

    def set_min_participantes(self, min_participantes: int) -> None:
        self.__min_participantes = min_participantes

    def set_max_participantes(self, max_participantes: int) -> None:
        self.__max_participantes = max_participantes

    def set_status(self, status: StatusEvento) -> None:
        self.__status = status

    def set_organizador(self, organizador: Organizador) -> None:
        self.__organizador = organizador