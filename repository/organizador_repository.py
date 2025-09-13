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
        if not novo_organizador.get_username() or not novo_organizador.get_senha():
            return (None, "Nome de usuário e senha são obrigatórios.")

        response_check = supabase.table('organizadores').select('id').eq('username', novo_organizador.get_username()).execute()

        if response_check.data:
            return (None, f"O nome de usuário '{novo_organizador.get_username()}' já existe.")

        response_insert = supabase.table('organizadores').insert({
            "username": novo_organizador.get_username(),
            "senha": novo_organizador.get_senha()
        }).execute()

        if response_insert.data:
            id_criado = response_insert.data[0]['id']
            novo_organizador.id = id_criado
            return (novo_organizador, f"Organizador '{novo_organizador.get_username()}' criado com sucesso!")
        else:
            error_message = response_insert.error.message if response_insert.error else "Erro desconhecido ao inserir dados."
            return (None, f"Falha ao criar organizador: {error_message}")
    except Exception as e:
        return (None, f"Ocorreu um erro inesperado no servidor: {e}")
