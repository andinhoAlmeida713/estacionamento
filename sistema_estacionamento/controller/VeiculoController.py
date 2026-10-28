from sqlmodel import Session, select
from fastapi import HTTPException, status
from app.entidades.models import Veiculo

class VeiculoController:
    @staticmethod
    def criar_veiculo(veiculo: Veiculo, db: Session) -> Veiculo:
        # Regra de Negócio: Placa única por estacionamento ativo
        statement = select(Veiculo).where(
            Veiculo.placa == veiculo.placa,
            Veiculo.estacionamento_id == veiculo.estacionamento_id,
            Veiculo.ativo == True
        )
        veiculo_existente = db.exec(statement).first()
        if veiculo_existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Um veículo com esta placa já está ativo neste estacionamento."
            )
            
        db.add(veiculo)
        db.commit()
        db.refresh(veiculo)
        return veiculo
