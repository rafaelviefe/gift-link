import os
from typing import List, Optional, Tuple

from dotenv import load_dotenv
from supabase import Client, create_client

from model.participante import Participante


class ParticipanteRepository:
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__supabase: Client = create_client(url, key)

    def criar(self, novo_participante: Participante) -> Tuple[Optional[Participante], str]:
        try:
            response_insert = (
                self.__supabase.table("participantes")
                .insert(
                    {
                        "username": novo_participante.get_username(),
                        "senha": novo_participante.get_senha(),
                    }
                )
                .execute()
            )

            if response_insert.data:
                id_criado = response_insert.data[0]["id"]
                novo_participante.set_id(id_criado)
                return (
                    novo_participante,
                    f"Participante '{novo_participante.get_username()}' criado com sucesso!",
                )
            else:
                return (None, f"Falha ao criar participante")
        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")

    def buscar_por_username(self, username: str) -> Tuple[Optional[Participante], str]:
        try:
            response = self.__supabase.table('participantes').select('*').eq('username', username).execute()

            if response.data:
                dados_participante = response.data[0]

                participante_encontrado = Participante(
                    id=dados_participante.get("id"),
                    username=dados_participante.get("username"),
                    senha=dados_participante.get("senha"),
                    elegivel=dados_participante.get("elegivel"),
                )
                return (participante_encontrado, f"Participante '{username}' encontrado com sucesso.")

            else:
                return (None, f"Participante com o nome de usuário '{username}' não encontrado.")

        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")

    def buscar_por_id(self, id: int) -> Tuple[Optional[Participante], str]:
        try:
            response = self.__supabase.table('participantes').select('*').eq('id', id).execute()

            if response.data:
                dados_participante = response.data[0]

                participante_encontrado = Participante(
                    id=dados_participante.get("id"),
                    username=dados_participante.get("username"),
                    senha=dados_participante.get("senha"),
                    elegivel=dados_participante.get("elegivel"),
                )
                return (participante_encontrado, f"Participante com ID '{id}' encontrado com sucesso.")

            else:
                return (None, f"Participante com ID:'{id}' não encontrado.")

        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")

    def listar(self) -> Tuple[List[Participante], str]:
        try:
            response = self.__supabase.table("participantes").select("*").execute()

            if response.data:
                participantes = []
                for item in response.data:
                    participante = Participante(
                        id=item["id"],
                        username=item["username"],
                        senha=item["senha"],
                        elegivel=item["elegivel"],
                    )
                    participantes.append(participante)
                return (participantes, "Participantes buscados com sucesso!")
            else:
                return ([], "Nenhum participante encontrado.")
        except Exception as e:
            return ([], f"Ocorreu um erro inesperado no servidor: {e}")

    def alterar_senha(self, username: str, nova_senha: str) -> Tuple[bool, str]:
        try:
            response = self.__supabase.table("participantes").update({"senha": nova_senha, "elegivel": True}).eq("username", username).execute()

            if response.data:
                return (True, f"Senha alterada com sucesso.")
            else:
                return (False, f"Participante com o nome de usuário '{username}' não encontrado.")

        except Exception as e:
            return (False, f"Ocorreu um erro inesperado no servidor: {e}")

    def buscar_elegiveis(self) -> Tuple[List[Participante], str]:
        """Busca todos os participantes elegíveis de um evento específico"""
        try:
            response = self.__supabase.table('participantes').select('*').eq('elegivel', True).execute()

            if response.data:
                participantes = []
                for dados in response.data:
                    participante = Participante(
                        id=dados.get('id'),
                        username=dados.get('username'),
                        senha=dados.get('senha'),
                        elegivel=dados.get('elegivel', False)
                    )
                    participantes.append(participante)

                return (participantes, f"Encontrados {len(participantes)} participantes elegíveis.")
            else:
                return ([], "Nenhum participante elegível encontrado.")

        except Exception as e:
            return ([], f"Ocorreu um erro inesperado no servidor: {e}")
