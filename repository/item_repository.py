import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional, Tuple, List
from model.item import Item
from model.participante import Participante

class ItemRepository:
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__supabase: Client = create_client(url, key)

    def criar(self, novo_item: Item) -> Tuple[Optional[Item], str]:
        try:
            response_insert = (
                self.__supabase.table("itens")
                .insert(
                    {
                        "nome": novo_item.get_nome(),
                        "preco": novo_item.get_preco(),
                        "id_participante": novo_item.get_id_participante(),
                    }
                )
                .execute()
            )

            if response_insert.data:
                id_criado = response_insert.data[0]["id"]
                novo_item.set_id(id_criado)
                return (
                    novo_item,
                    f"Item '{novo_item.get_nome()}' adicionado com sucesso!",
                )
            else:
                return (None, "Falha ao adicionar item.")
        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")

    def remover(self, item_id: int) -> Tuple[bool, str]:
        try:
            response = (
                self.__supabase.table("itens")
                .delete()
                .eq("id", item_id)
                .execute()
            )

            if response.data:
                return (True, "Item removido com sucesso.")
            else:
                return (False, "Falha ao remover item. Item não encontrado.")
        except Exception as e:
            return (False, f"Ocorreu um erro inesperado no servidor: {e}")

    def listar_por_participante(
        self, participante: Participante
    ) -> Tuple[List[Item], str]:
        try:
            id_participante = participante.get_id()
            response = (
                self.__supabase.table("itens")
                .select("*")
                .eq("id_participante", id_participante)
                .order("nome")
                .execute()
            )

            if response.data:
                itens = []
                for item_data in response.data:
                    item = Item(
                        id=item_data.get("id"),
                        nome=item_data.get("nome"),
                        preco=item_data.get("preco"),
                        participante=participante,
                    )
                    itens.append(item)
                return (itens, "Itens buscados com sucesso!")
            else:
                return ([], "Nenhum item encontrado para este participante.")
        except Exception as e:
            return ([], f"Ocorreu um erro inesperado no servidor: {e}")