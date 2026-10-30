from fastapi import Header, HTTPException, status, Depends
from sqlmodel import Session
from typing import Generator
from app.db import get_session

def obter_db() -> Generator[Session, None, None]:
    """
    Encapsula o get_session do banco de dados para ser injetado 
    centralizadamente através do módulo de dependências.
    """
    yield from get_session()

def verificar_estacionamento_ativo(
    x_estacionamento_id: int = Header(..., alias="X-Estacionamento-ID")
) -> int:
    """
    Dependência de segurança que valida se a requisição possui o cabeçalho 
    'X-Estacionamento-ID' informado, impedindo requisições sem contexto de filial.
    """
    if not x_estacionamento_id or x_estacionamento_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O cabeçalho 'X-Estacionamento-ID' é obrigatório e deve conter um ID válido."
        )
    return x_estacionamento_id
