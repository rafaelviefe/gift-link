from typing import Optional, Tuple
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from model.participante import Participante

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)

def criar_participante(novo_participante : Participante) -> Tuple[Optional[Participante], str]:
    try:
        response_check = supabase.table('participantes').select('id').eq('username', novo_participante.get_username()).execute()

        if response_check.data:
            return (None, f"O nome de usuário '{novo_participante.get_username()}' já existe.")

        response_insert = supabase.table('participantes').insert({
            "username": novo_participante.get_username(),
            "senha": novo_participante.get_senha()
        }).execute()

        if response_insert.data:
            id_criado = response_insert.data[0]['id']
            novo_participante.set_id(id_criado)
            return (novo_participante, f"Participante '{novo_participante.get_username()}' criado com sucesso!")
        else:
            error_message = response_insert.error.message if response_insert.error else "Erro desconhecido ao inserir dados."
            return (None, f"Falha ao criar participante: {error_message}")
    except Exception as e:
        return (None, f"Ocorreu um erro inesperado no servidor: {e}")
