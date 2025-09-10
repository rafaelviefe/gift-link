import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Tuple
from model.chave import Chave

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def verificar_chave(chave_para_verificar: Chave) -> Tuple[bool, str]:

    try:
        chave_id = chave_para_verificar.get_id()
        response = supabase.table('chave').select('id').eq('id', chave_id).execute()

        return (bool(response.data), "Chave de acesso válida." if response.data else "Chave de acesso inválida.")

    except Exception as e:
        return (False, f"Ocorreu um erro inesperado no servidor: {e}")
