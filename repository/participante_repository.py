from typing import Optional, Tuple
from dotenv import load_dotenv
from supabase import create_client, Client
import os
from model.participante import Participante

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)


def criar_participante(
    novo_participante: Participante,
) -> Tuple[Optional[Participante], str]:
    try:
        response_check = (
            supabase.table("participantes")
            .select("id")
            .eq("username", novo_participante.get_username())
            .execute()
        )

        if response_check.data:
            return (
                None,
                f"O nome de usuário '{novo_participante.get_username()}' já existe.",
            )

        response_insert = (
            supabase.table("participantes")
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
            error_message = (
                response_insert.error.message
                if response_insert.error
                else "Erro desconhecido ao inserir dados."
            )
            return (None, f"Falha ao criar participante: {error_message}")
    except Exception as e:
        return (None, f"Ocorreu um erro inesperado no servidor: {e}")

def buscar_participante(username: str) -> Tuple[Optional[Participante], str]:
    try:
        response = supabase.table('participantes').select('*').eq('username', username).execute()

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
            if response.error:
                 return (None, f"Falha ao buscar participante: {response.error.message}")
            return (None, f"Participante com o nome de usuário '{username}' não encontrado.")
        
    except Exception as e:
        return (None, f"Ocorreu um erro inesperado no servidor: {e}")

def listar_participantes() -> Tuple[list, str]:
    try:
        response = supabase.table("participantes").select("*").execute()

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

def alterar_senha_participante(username: str, nova_senha: str) -> Tuple[bool, str]:
    try:
        response = supabase.table("participantes").update({"senha": nova_senha}).eq("username", username).execute()

        if response.data:
            return (True, f"Senha alterada com sucesso.")
        else:
            if response.error:
                return (False, f"Falha ao alterar a senha: {response.error.message}")
            return (False, f"Participante com o nome de usuário '{username}' não encontrado.")

    except Exception as e:
        return (False, f"Ocorreu um erro inesperado no servidor: {e}")