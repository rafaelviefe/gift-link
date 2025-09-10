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
        if not novo_organizador.username or not novo_organizador.senha or len(novo_organizador.senha) < 6:
            return (None, "Nome de usuário e senha são obrigatórios. A senha deve ter no mínimo 6 caracteres.")

        response_check = supabase.table('organizadores').select('id').eq('username', novo_organizador.username).execute()
        
        if response_check.data:
            return (None, f"O nome de usuário '{novo_organizador.username}' já existe.")

        response_insert = supabase.table('organizadores').insert({
            "username": novo_organizador.username,
            "senha": novo_organizador.senha
        }).execute()

        if response_insert.data:
            id_criado = response_insert.data[0]['id']
            novo_organizador.id = id_criado
            return (novo_organizador, f"Organizador '{novo_organizador.username}' criado com sucesso!")
        else:
            error_message = response_insert.error.message if response_insert.error else "Erro desconhecido ao inserir dados."
            return (None, f"Falha ao criar organizador: {error_message}")
    except Exception as e:
        return (None, f"Ocorreu um erro inesperado no servidor: {e}")