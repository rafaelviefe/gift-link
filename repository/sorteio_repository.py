import os
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
from supabase import Client, create_client

from model.sorteio import Sorteio


class SorteioRepository:
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__supabase: Client = create_client(url, key)

    def salvar_sorteio(self, lista_sorteios: List[Dict]) -> Tuple[bool, str]:
        """
        Recebe uma lista de dicionários formatados para o Supabase.
        Ex: [{"id_evento": 1, "id_participante_origem": 2, "id_participante_destino": 3}, ...]
        """
        try:
            self.__supabase.table("sorteios").insert(lista_sorteios).execute()
            return True, "Sorteio salvo com sucesso!"
        except Exception as e:
            return False, f"Erro ao persistir sorteio: {e}"

    def buscar_amigo_secreto(self, id_evento: int, id_participante: int) -> Tuple[Optional[str], str]:
        """
        Busca quem um participante específico tirou em um evento específico.
        Retorna o NOME (username) do amigo secreto.
        """
        try:
            response = (
                self.__supabase.table("sorteios")
                .select("participantes!id_participante_destino(username)")
                .eq("id_evento", id_evento)
                .eq("id_participante_origem", id_participante)
                .execute()
            )

            if response.data:
                # O supabase retorna aninhado devido à Foreign Key
                nome_amigo = response.data[0]['participantes']['username']
                return nome_amigo, "Amigo encontrado."
            else:
                return None, "Sorteio ainda não realizado ou você não está neste evento."
        except Exception as e:
            return None, f"Erro ao buscar amigo secreto: {e}"

    def listar_por_participante(self, id_participante: int) -> Tuple[List[Dict], str]:
            """
            Retorna uma lista de dicionários contendo o nome do evento, status e o nome do amigo tirado.
            """
            try:
                # Busca na tabela sorteios onde o usuário é a origem (quem tirou)
                # Fazemos o join com a tabela de eventos para pegar o nome e status
                # E com a tabela participantes (destino) para já pegar o nome de quem ele tirou
                response = (
                    self.__supabase.table("sorteios")
                    .select("id_evento, eventos(nome, status), participantes!id_participante_destino(username)")
                    .eq("id_participante_origem", id_participante)
                    .execute()
                )

                if response.data:
                    resultados = []
                    for registro in response.data:
                        # O Supabase retorna os joins como dicionários aninhados
                        evento_nome = registro['eventos']['nome']
                        evento_status = registro['eventos']['status']
                        amigo_nome = registro['participantes']['username']

                        resultados.append({
                            "evento": evento_nome,
                            "status": evento_status,
                            "amigo_secreto": amigo_nome
                        })
                    return resultados, "Eventos encontrados com sucesso."
                else:
                    return [], "Você ainda não participou de nenhum sorteio."

            except Exception as e:
                return [], f"Erro ao buscar eventos: {e}"

    def listar_por_evento(self, id_evento: int) -> Tuple[List[Dict], str]:
            """
            Retorna TODOS os pares de um evento (A visão do Organizador).
            """
            try:
                # Precisamos de aliases para distinguir origem e destino,
                # pois ambos apontam para a tabela 'participantes'
                response = (
                    self.__supabase.table("sorteios")
                    .select(
                        "id_participante_origem, "
                        "origem:participantes!id_participante_origem(username), "
                        "destino:participantes!id_participante_destino(username)"
                    )
                    .eq("id_evento", id_evento)
                    .execute()
                )

                if response.data:
                    pares = []
                    for registro in response.data:
                        nome_quem_tirou = registro['origem']['username']
                        nome_quem_foi_tirado = registro['destino']['username']

                        pares.append({
                            "quem_tirou": nome_quem_tirou,
                            "quem_foi_tirado": nome_quem_foi_tirado
                        })
                    return pares, "Mapeamento carregado com sucesso."
                else:
                    return [], "Nenhum sorteio encontrado para este evento."

            except Exception as e:
                return [], f"Erro ao buscar mapeamento: {e}"
