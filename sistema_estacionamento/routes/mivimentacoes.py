from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from decimal import Decimal
from app.db import get_session
from app.entidades.models import Movimentacao
from app.controller import MovimentacaoController

router = APIRouter(prefix="/movimentacoes", tags=["Movimentações"])

@router.post("/entrada", response_model=Movimentacao, status_code=status.HTTP_201_CREATED)
def registrar_entrada(movimentacao: Movimentacao, db: Session = Depends(get_session)):
    """
    Registra o check-in (entrada) de um veículo no pátio através do MovimentacaoController.
    """
    return MovimentacaoController.registrar_entrada(movimentacao, db)

@router.post("/saida/{movimentacao_id}", response_model=Movimentacao)
def registrar_saida(
    movimentacao_id: int, 
    desconto: Decimal = Decimal("0.00"), 
    db: Session = Depends(get_session)
):
    """
    Registra o check-out (saída) de um veículo, realizando o cálculo 
    automatizado de valores e frações de tempo no MovimentacaoController.
    """
    return MovimentacaoController.registrar_saida(movimentacao_id, desconto, db)
