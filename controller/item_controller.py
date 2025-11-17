from typing import Tuple, Optional, List
from model.item import Item
from model.participante import Participante
from repository.item_repository import ItemRepository

class ItemController:
    def __init__(self):
        self.__item_repository = ItemRepository()

    def registrar(
        self, nome: str, preco_str: str, participante: Participante
    ) -> Tuple[Optional[Item], str]:

        if not nome:
            return (None, "O nome do item é obrigatório.")

        try:
            preco = float(preco_str.replace(",", "."))
            if preco <= 0:
                return (None, "O preço deve ser um valor positivo.")
        except ValueError:
            return (None, "O preço informado é inválido. Use um número (ex: 29.90).")

        novo_item = Item(nome=nome, preco=preco, participante=participante)
        
        return self.__item_repository.criar(novo_item)

    def remover(self, item_id: int) -> Tuple[bool, str]:
        if not item_id:
            return (False, "Nenhum item selecionado para remoção.")
        return self.__item_repository.remover(item_id)

    def listar_por_participante(
        self, participante: Participante
    ) -> Tuple[List[Item], str]:
        return self.__item_repository.listar_por_participante(participante)