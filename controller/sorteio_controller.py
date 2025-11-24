import random
from typing import Dict, List, Tuple

from model.evento import Evento
from model.participante import Participante
from model.status_evento import StatusEvento
from repository.evento_repository import EventoRepository
from repository.sorteio_repository import SorteioRepository


class SorteioController:
    def __init__(self):
        self.__sorteio_repository = SorteioRepository()
        self.__evento_repository = EventoRepository()

    def realizar_sorteio(self, evento: Evento, participantes_selecionados: List[Participante]) -> Tuple[bool, str]:
        if evento.get_status() != StatusEvento.PREPARANDO:
            return False, f"Este evento já está com status '{evento.get_status().value}' e não pode ser sorteado novamente."

        qtd = len(participantes_selecionados)
        min_p = evento.get_min_participantes()
        max_p = evento.get_max_participantes()

        # 1. Validação: Mínimo e Máximo
        if qtd < min_p:
            return False, f"Quantidade insuficiente de participantes. Mínimo: {min_p}, Selecionados: {qtd}."

        if qtd > max_p:
            return False, f"Quantidade excede o máximo permitido. Máximo: {max_p}, Selecionados: {qtd}."

        # 2. Validação: Número Par (Requisito do usuário)
        if qtd % 2 != 0:
            return False, f"O número de participantes deve ser par. Selecionados: {qtd}."

        # 3. Algoritmo de Sorteio (Lógica Circular para garantir que ninguém se tire)
        # Embaralha a lista
        random.shuffle(participantes_selecionados)

        pares_para_salvar = []

        for i in range(qtd):
            participante_atual = participantes_selecionados[i]
            # O amigo secreto é o próximo da lista (o último pega o primeiro)
            indice_amigo = (i + 1) % qtd
            amigo_secreto = participantes_selecionados[indice_amigo]

            # Monta o objeto para o Repositório
            pares_para_salvar.append({
                "id_evento": evento.get_id(),
                "id_participante_origem": participante_atual.get_id(),
                "id_participante_destino": amigo_secreto.get_id()
            })

        sucesso, msg = self.__sorteio_repository.salvar_sorteio(pares_para_salvar)

        if sucesso:
            evento.set_status(StatusEvento.SORTEADO)
            self.__evento_repository.editar(evento) # Reutilizando o repo existente para salvar status
            return True, "Sorteio realizado com sucesso! Os participantes já podem ver seus amigos secretos."
        else:
            return False, msg

    def verificar_quem_tirei(self, id_evento: int, id_participante: int) -> str:
        nome_amigo, msg = self.__sorteio_repository.buscar_amigo_secreto(id_evento, id_participante)
        if nome_amigo:
            return f"🎉 Você tirou: {nome_amigo}!"
        else:
            return f"Informação não disponível: {msg}"

    def listar_meus_sorteios(self, participante: Participante) -> Tuple[List[Dict], str]:
            if not participante or not participante.get_id():
                return [], "Participante inválido."

            return self.__sorteio_repository.listar_por_participante(participante.get_id())

    def ver_mapeamento_geral(self, evento: Evento) -> Tuple[List[Dict], str]:
            return self.__sorteio_repository.listar_por_evento(evento.get_id())
