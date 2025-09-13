import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Tuple, Optional
from model.organizador import Organizador

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def criar_organizador(novo_organizador: Organizador) -> Tuple[Optional[Organizador], str]:
    try:
        response_check = supabase.table('organizadores').select('id').eq('username', novo_organizador.get_username()).execute()

        if response_check.data:
            return (None, f"O nome de usuário '{novo_organizador.get_username()}' já existe.")

        response_insert = supabase.table('organizadores').insert({
            "username": novo_organizador.get_username(),
            "senha": novo_organizador.get_senha()
        }).execute()

        if response_insert.data:
            id_criado = response_insert.data[0]['id']
            novo_organizador.set_id(id_criado)
            return (novo_organizador, f"Organizador '{novo_organizador.get_username()}' criado com sucesso!")
        else:
            return (None, f"Falha ao criar organizador")
            
    except Exception as e:
        return (None, f"Ocorreu um erro inesperado no servidor: {e}")

def buscar_organizador(username: str) -> Tuple[Optional[Organizador], str]:
    try:
        response = supabase.table('organizadores').select('*').eq('username', username).execute()

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