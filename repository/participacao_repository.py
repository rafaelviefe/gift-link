import os
from typing import List, Tuple, Optional
from dotenv import load_dotenv
from supabase import Client, create_client
from model.participacao import Participacao
from model.evento import Evento
from model.participante import Participante
from model.status_evento import StatusEvento
from repository.participante_repository import ParticipanteRepository
from repository.organizador_repository import OrganizadorRepository

class ParticipacaoRepository:
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__supabase: Client = create_client(url, key)
        self.__participante_repository = ParticipanteRepository()
        self.__organizador_repository = OrganizadorRepository()

    def adicionar(self, evento: Evento, participante: Participante) -> Tuple[bool, str]:
        try:
            dados = {
                "id_evento": evento.get_id(),
                "id_participante": participante.get_id()
            }
            self.__supabase.table("participacoes").insert(dados).execute()
            return True, "Participante adicionado ao evento com sucesso!"
        except Exception as e:
            return False, f"Erro ao adicionar participante: {e}"

    def remover(self, evento: Evento, participante: Participante) -> Tuple[bool, str]:
        try:
            self.__supabase.table("participacoes")\
                .delete()\
                .eq("id_evento", evento.get_id())\
                .eq("id_participante", participante.get_id())\
                .execute()
            return True, "Participante removido do evento."
        except Exception as e:
            return False, f"Erro ao remover participante: {e}"

    def listar_por_evento(self, evento: Evento) -> Tuple[List[Participante], str]:
        try:
            response = self.__supabase.table("participacoes")\
                .select("id_participante")\
                .eq("id_evento", evento.get_id())\
                .execute()

            if response.data:
                participantes = []
                for item in response.data:
                    p_id = item.get("id_participante")
                    p, _ = self.__participante_repository.buscar_por_id(p_id)
                    if p:
                        participantes.append(p)
                return participantes, "Participantes listados com sucesso."
            else:
                return [], "Nenhum participante vinculado a este evento."
        except Exception as e:
            return [], f"Erro ao buscar participantes: {e}"

    def listar_por_participante(self, participante: Participante) -> Tuple[List[Participacao], str]:
        try:
            response = self.__supabase.table("participacoes")\
                .select("*, eventos(*)")\
                .eq("id_participante", participante.get_id())\
                .execute()

            if response.data:
                lista_participacoes = []
                for item in response.data:
                    dados_evento = item.get("eventos")
                    
                    if not dados_evento:
                        continue

                    id_organizador = dados_evento.get("id_organizador")
                    organizador, _ = self.__organizador_repository.buscar_por_id(id_organizador)

                    evento_obj = Evento(
                        id=dados_evento.get("id"),
                        nome=dados_evento.get("nome"),
                        descricao=dados_evento.get("descricao"),
                        min_participantes=dados_evento.get("min_participantes"),
                        max_participantes=dados_evento.get("max_participantes"),
                        status=StatusEvento(dados_evento.get("status")),
                        organizador=organizador
                    )

                    nova_participacao = Participacao(
                        id=item.get("id"),
                        evento=evento_obj,
                        participante=participante
                    )
                    lista_participacoes.append(nova_participacao)
                
                return lista_participacoes, "Eventos do participante encontrados."
            else:
                return [], "Você não está participando de nenhum evento."
        except Exception as e:
            return [], f"Erro ao buscar eventos do participante: {e}"