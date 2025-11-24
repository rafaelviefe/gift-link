from typing import Optional

from model.evento import Evento
from model.participante import Participante


class Sorteio:
    def __init__(
        self,
        evento: Evento,
        participante_origem: Participante,
        participante_destino: Participante,
        id: Optional[int] = None
    ):
        self.__id = id
        self.__evento = evento
        self.__participante_origem = participante_origem
        self.__participante_destino = participante_destino

    def get_id(self) -> Optional[int]:
        return self.__id

    def get_evento(self) -> Evento:
        return self.__evento

    def get_participante_origem(self) -> Participante:
        return self.__participante_origem

    def get_participante_destino(self) -> Participante:
        return self.__participante_destino
