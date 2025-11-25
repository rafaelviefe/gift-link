from typing import Optional
from model.evento import Evento
from model.participante import Participante

class Participacao:
    def __init__(self, evento: Evento, participante: Participante, id: Optional[int] = None):
        self.__id = id
        self.__evento = evento
        self.__participante = participante

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_evento(self) -> Evento:
        return self.__evento

    def get_participante(self) -> Participante:
        return self.__participante

    def set_id(self, id: int) -> None:
        self.__id = id