from fastapi import APIRouter, Depends, status, Body
from sqlmodel import Session
from typing import List
from app.db import get_session
from app.entidades.models import Usuario
from app.controller import UsuarioController

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def cadastrar_usuario(
    usuario: Usuario, 
    senha_pura: str = Body(..., embed=True, description="Senha em texto limpo para criptografia"),
    db: Session = Depends(get_session)
):
    """
    Cadastra um novo usuário (administrador ou operador) no sistema.
    A senha enviada no corpo da requisição é criptografada automaticamente antes de salvar.
    """
    return UsuarioController.criar_usuario(usuario, senha_pura, db)

@router.get("/{usuario_id}", response_model=Usuario)
def buscar_usuario_por_id(usuario_id: int, db: Session = Depends(get_session)):
    """
    Busca os detalhes cadastrais de um usuário ativo através do ID.
    """
    return UsuarioController.buscar_por_id(usuario_id, db)
