import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Tuple, Optional
from model.organizador import Organizador

class OrganizadorRepository:
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__supabase: Client = create_client(url, key)

    def criar_organizador(self, novo_organizador: Organizador) -> Tuple[Optional[Organizador], str]:
        username = novo_organizador.get_username()
        senha = novo_organizador.get_senha()

        try:
            organizador_existente, _ = self.buscar_organizador(username)

            if organizador_existente:
                return (None, f"O nome de usuário '{username}' já existe.")

            response_insert = self.__supabase.table('organizadores').insert({
                "username": username,
                "senha": senha
            }).execute()

            if response_insert.data:
                id_criado = response_insert.data[0]['id']
                novo_organizador.set_id(id_criado)
                return (novo_organizador, f"Organizador '{username}' criado com sucesso!")
            else:
                return (None, "Falha ao criar organizador")
                
        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")

    def buscar_organizador(self, username: str) -> Tuple[Optional[Organizador], str]:
        try:
            response = self.__supabase.table('organizadores').select('*').eq('username', username).execute()

            if response.data:
                dados_organizador = response.data[0]
                
                organizador_encontrado = Organizador(
                    id=dados_organizador.get('id'),
                    username=dados_organizador.get('username'),
                    senha=dados_organizador.get('senha')
                )
                return (organizador_encontrado, f"Organizador '{username}' encontrado com sucesso.")
            
            else:
                return (None, f"Organizador com o nome de usuário '{username}' não encontrado.")
            
        except Exception as e:
            return (None, f"Ocorreu um erro inesperado no servidor: {e}")