from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from typing import List
from app.db import get_session
from app.entidades.models import Veiculo
from app.controller import VeiculoController

router = APIRouter(prefix="/veiculos", tags=["Veículos"])

@router.post("/", response_model=Veiculo, status_code=status.HTTP_201_CREATED)
def cadastrar_veiculo(veiculo: Veiculo, db: Session = Depends(get_session)):
    """
    Cadastra um novo veículo utilizando as regras de validação do VeiculoController.
    """
    return VeiculoController.criar_veiculo(veiculo, db)

@router.get("/{estacionamento_id}", response_model=List[Veiculo])
def listar_veiculos(estacionamento_id: int, db: Session = Depends(get_session)):
    """
    Lista todos os veículos cadastrados de um determinado estacionamento.
    """
    statement = select(Veiculo).where(Veiculo.estacionamento_id == estacionamento_id)
    return db.exec(statement).all()
