import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Tuple
from model.chave import Chave

class ChaveRepository:
    def __init__(self):
        load_dotenv()
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.__supabase: Client = create_client(url, key)

    def verificar_chave(self, chave_para_verificar: Chave) -> Tuple[bool, str]:
        try:
            chave_id = chave_para_verificar.get_id()
            response = self.__supabase.table('chave').select('id').eq('id', chave_id).execute()

            if response.data:
                return (True, "Chave de acesso válida.")
            else:
                return (False, "Chave de acesso inválida.")

        except Exception as e:
            return (False, f"Ocorreu um erro inesperado no servidor: {e}")