from sqlmodel import Session, select
from datetime import datetime
from decimal import Decimal
from math import ceil
from fastapi import HTTPException, status
from app.entidades.models import Movimentacao, StatusMovimentacao, TabelaPreco

class MovimentacaoController:
    @staticmethod
    def registrar_entrada(movimentacao: Movimentacao, db: Session) -> Movimentacao:
        # Regra de Negócio: Impede duplicidade de veículo no pátio
        statement = select(Movimentacao).where(
            Movimentacao.veiculo_id == movimentacao.veiculo_id,
            Movimentacao.status == StatusMovimentacao.aberta
        )
        em_aberto = db.exec(statement).first()
        if em_aberto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este veículo já possui uma movimentação em aberto."
            )
        
        movimentacao.entrada_em = datetime.utcnow()
        movimentacao.status = StatusMovimentacao.aberta
        
        db.add(movimentacao)
        db.commit()
        db.refresh(movimentacao)
        return movimentacao

    @staticmethod
    def registrar_saida(movimentacao_id: int, desconto: Decimal, db: Session) -> Movimentacao:
        mov = db.get(Movimentacao, movimentacao_id)
        if not mov or mov.status != StatusMovimentacao.aberta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movimentação ativa não encontrada."
            )
        
        tabela = db.get(TabelaPreco, mov.tabela_preco_id)
        if not tabela:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Tabela de preços não vinculada à movimentação."
            )
        
        mov.saida_em = datetime.utcnow()
        mov.status = StatusMovimentacao.finalizada
        mov.desconto = desconto
        
        # --- ALGORITMO DE CÁLCULO DE VALOR ---
        duracao = mov.saida_em - mov.entrada_em
        minutos_totais = int(duracao.total_seconds() / 60)
        
        # 1. Verifica tempo de tolerância
        if minutos_totais <= tabela.minutos_tolerancia:
            mov.valor_calculado = Decimal("0.00")
        
        # 2. Verifica cobrança por Diária (se configurada)
        elif tabela.valor_diaria and minutos_totais >= 720:  # Exemplo: Mais de 12 horas vira diária
            mov.valor_calculado = tabela.valor_diaria
            mov.tipo_cobranca = "diaria"
            
        # 3. Verifica cobrança Fracionada
        elif tabela.cobrar_fracao and tabela.minutos_fracao > 0:
            fracoes = ceil(minutos_totais / tabela.minutos_fracao)
            mov.valor_calculado = Decimal(fracoes) * tabela.valor_fracao
            mov.tipo_cobranca = "hora"
            
        # 4. Cobrança padrão por hora cheia
        else:
            horas_cheias = ceil(minutos_totais / 60)
            mov.valor_calculado = Decimal(horas_cheias) * tabela.valor_hora
            mov.tipo_cobranca = "hora"
            
        # Aplica o desconto de forma segura
        mov.valor_cobrado = max(Decimal("0.00"), mov.valor_calculado - mov.desconto)
        
        db.add(mov)
        db.commit()
        db.refresh(mov)
        return mov
