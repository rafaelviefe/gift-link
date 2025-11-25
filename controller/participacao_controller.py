from typing import List, Tuple, Optional
from model.participacao import Participacao
from model.participante import Participante
from model.evento import Evento
from model.status_evento import StatusEvento
from repository.participacao_repository import ParticipacaoRepository
from repository.evento_repository import EventoRepository
from repository.participante_repository import ParticipanteRepository

class ParticipacaoController:
    def __init__(self):
        self.__participacao_repository = ParticipacaoRepository()
        self.__evento_repository = EventoRepository()
        self.__participante_repository = ParticipanteRepository()

    def adicionar_participante_evento(self, id_evento: int, id_participante: int) -> Tuple[bool, str]:
        eventos, _ = self.__evento_repository.listar()
        evento_encontrado = None
        for e in eventos:
            if e.get_id() == id_evento:
                evento_encontrado = e
                break
        
        if not evento_encontrado:
            return False, "Evento não encontrado."

        if evento_encontrado.get_status() == StatusEvento.FINALIZADO:
             return False, "Não é possível adicionar participantes a um evento finalizado."

        participante_encontrado, _ = self.__participante_repository.buscar_por_id(id_participante)
        if not participante_encontrado:
             return False, "Participante não encontrado."

        participantes_existentes, _ = self.__participacao_repository.listar_por_evento(evento_encontrado)
        for p in participantes_existentes:
            if p.get_id() == id_participante:
                return False, "Participante já está vinculado a este evento."

        return self.__participacao_repository.adicionar(evento_encontrado, participante_encontrado)

    def remover_participante_evento(self, id_evento: int, id_participante: int) -> Tuple[bool, str]:
        eventos, _ = self.__evento_repository.listar()
        evento_encontrado = None
        for e in eventos:
            if e.get_id() == id_evento:
                evento_encontrado = e
                break
        
        if not evento_encontrado:
            return False, "Evento não encontrado."

        if evento_encontrado.get_status() != StatusEvento.PREPARANDO:
             return False, "Só é possível remover participantes enquanto o evento está 'Preparando'."

        participante_encontrado, _ = self.__participante_repository.buscar_por_id(id_participante)
        if not participante_encontrado:
             return False, "Participante não encontrado."
             
        return self.__participacao_repository.remover(evento_encontrado, participante_encontrado)

    def listar_participantes_do_evento(self, id_evento: int) -> Tuple[List[Participante], str]:
        eventos, _ = self.__evento_repository.listar()
        evento_encontrado = None
        for e in eventos:
            if e.get_id() == id_evento:
                evento_encontrado = e
                break
        
        if not evento_encontrado:
            return [], "Evento não encontrado."
            
        return self.__participacao_repository.listar_por_evento(evento_encontrado)

    def listar_eventos_do_participante(self, participante: Participante) -> Tuple[List[Participacao], str]:
        return self.__participacao_repository.listar_por_participante(participante)