from typing import Tuple, Optional, List
from model.evento import Evento
from model.organizador import Organizador
from repository.evento_repository import EventoRepository

class EventoController:
    def __init__(self):
        self.__evento_repository = EventoRepository()

    def registrar(
        self,
        nome: str,
        descricao: str,
        min_participantes: int,
        max_participantes: int,
        organizador: Organizador,
    ) -> Tuple[Optional[Evento], str]:

        try:
            min_p = int(min_participantes)
            max_p = int(max_participantes)
        except ValueError:
            return (None, "Os valores de mínimo e máximo de participantes devem ser números inteiros.")

        if not nome:
            return (None, "O nome do evento é obrigatório.")
        
        if min_p <= 0 or max_p <= 0:
             return (None, "Os valores de mínimo e máximo de participantes devem ser positivos.")

        if min_p > max_p:
            return (None, "O número mínimo de participantes não pode ser maior que o máximo.")

        novo_evento = Evento(
            nome=nome,
            descricao=descricao,
            min_participantes=min_p,
            max_participantes=max_p,
            organizador=organizador,
        )
        
        return self.__evento_repository.criar(novo_evento)

    def editar(self, evento: Evento, novo_nome: str, nova_descricao: str) -> Tuple[Optional[Evento], str]:
        if not novo_nome:
            return (None, "O nome do evento é obrigatório.")

        evento.set_nome(novo_nome)
        evento.set_descricao(nova_descricao)

        return self.__evento_repository.editar(evento)

    def listar(self) -> Tuple[List[Evento], str]:
        eventos, mensagem = self.__evento_repository.listar()
        return eventos, mensagem