import os
from typing import List, Optional, Tuple

from dotenv import load_dotenv
from supabase import Client, create_client

from model.evento import Evento
from model.status_evento import StatusEvento
from repository.organizador_repository import OrganizadorRepository


class EventoRepository:
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__supabase: Client = create_client(url, key)
        self.__organizador_repository = OrganizadorRepository()

    def criar(self, novo_evento: Evento) -> Tuple[Optional[Evento], str]:
        try:
            response_insert = (
                self.__supabase.table("eventos")
                .insert(
                    {
                        "nome": novo_evento.get_nome(),
                        "descricao": novo_evento.get_descricao(),
                        "min_participantes": novo_evento.get_min_participantes(),
                        "max_participantes": novo_evento.get_max_participantes(),
                        "status": novo_evento.get_status().value,
                        "id_organizador": novo_evento.get_id_organizador(),
                    }
                )
                .execute()
            )

            if response_insert.data:
                id_criado = response_insert.data[0]["id"]
                novo_evento.set_id(id_criado)
                return (
                    novo_evento,
                    f"Evento '{novo_evento.get_nome()}' criado com sucesso!",
                )
            else:
                return (None, f"Falha ao criar evento")
        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")

    def editar(self, evento: Evento) -> Tuple[Optional[Evento], str]:
        try:
            response_update = (
                self.__supabase.table("eventos")
                .update(
                    {
                        "nome": evento.get_nome(),
                        "descricao": evento.get_descricao(),
                        "status": evento.get_status().value,
                    }
                )
                .eq("id", evento.get_id())
                .execute()
            )

            if response_update.data:
                return (evento, "Evento atualizado com sucesso!")
            else:
                return (None, "Falha ao atualizar evento")
        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")

    def listar(self) -> Tuple[List[Evento], str]:
        try:
            response = self.__supabase.table("eventos").select("*").execute()

            if response.data:
                eventos = []
                for item in response.data:

                    id_organizador = item.get("id_organizador")
                    organizador, msg = self.__organizador_repository.buscar_por_id(id_organizador)

                    if not organizador:
                        continue

                    evento = Evento(
                        id=item.get("id"),
                        nome=item.get("nome"),
                        descricao=item.get("descricao"),
                        min_participantes=item.get("min_participantes"),
                        max_participantes=item.get("max_participantes"),
                        status=StatusEvento(item.get("status")),
                        organizador=organizador,
                    )
                    eventos.append(evento)
                return (eventos, "Eventos buscados com sucesso!")
            else:
                return ([], "Nenhum evento encontrado.")
        except Exception as e:
            return ([], f"Ocorreu um erro inesperado no servidor: {e}")
