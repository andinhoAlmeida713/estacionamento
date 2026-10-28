from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List
from app.dependencies import obter_db, verificar_estacionamento_ativo
from app.entidades.models import Cliente

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(cliente: Cliente, db: Session = Depends(obter_db)):
    """
    Insere um novo cliente no banco de dados.
    """
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.get("/", response_model=List[Cliente])
def listar_clientes_do_estacionamento(
    db: Session = Depends(obter_db),
    estacionamento_id: int = Depends(verificar_estacionamento_ativo)
):
    """
    Retorna a listagem de clientes associados ao ID do estacionamento.
    O ID do estacionamento é pego e validado automaticamente do cabeçalho da requisição (Header).
    """
    # Faz o SELECT filtrando as colunas pelo ID validado na dependência
    statement = select(Cliente).where(Cliente.estacionamento_id == estacionamento_id)
    return db.exec(statement).all()
