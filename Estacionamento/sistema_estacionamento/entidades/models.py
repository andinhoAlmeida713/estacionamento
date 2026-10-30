from sqlmodel import Field, SQLModel
from enum import Enum
from typing import Optional
from datetime import datetime, date
from decimal import Decimal

# ----------------------------------------------------------------------------
# ENUMS (Idênticos aos ENUMs definidos no seu banco MySQL)
# ----------------------------------------------------------------------------
class PerfilUsuario(str, Enum):
    administrador = "administrador"
    operador = "operador"

class TipoPessoa(str, Enum):
    fisica = "fisica"
    juridica = "juridica"

class TipoVeiculo(str, Enum):
    carro = "carro"
    moto = "moto"
    utilitario = "utilitario"
    caminhao = "caminhao"
    outro = "outro"

class StatusContrato(str, Enum):
    ativo = "ativo"
    suspenso = "suspenso"
    encerrado = "encerrado"

class TipoCobranca(str, Enum):
    hora = "hora"
    diaria = "diaria"
    mensal = "mensal"

class StatusMovimentacao(str, Enum):
    aberta = "aberta"
    finalizada = "finalizada"
    cancelada = "cancelada"

class FormaPagamento(str, Enum):
    dinheiro = "dinheiro"
    pix = "pix"
    debito = "debito"
    credito = "credito"
    transferencia = "transferencia"
    outro = "outro"

class StatusPagamento(str, Enum):
    pendente = "pendente"
    pago = "pago"
    cancelado = "cancelado"


# ----------------------------------------------------------------------------
# MODELOS DE TABELAS DO BANCO DE DADOS
# ----------------------------------------------------------------------------

class Estacionamento(SQLModel, table=True):
    __tablename__ = "estacionamentos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str = Field(max_length=150, nullable=False)
    cnpj: Optional[str] = Field(default=None, max_length=18, unique=True)
    telefone: Optional[str] = Field(default=None, max_length=25)
    email: Optional[str] = Field(default=None, max_length=150)
    cep: Optional[str] = Field(default=None, max_length=10)
    endereco: Optional[str] = Field(default=None, max_length=200)
    numero: Optional[str] = Field(default=None, max_length=20)
    bairro: Optional[str] = Field(default=None, max_length=100)
    cidade: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[str] = Field(default=None, max_length=2)
    ativo: bool = Field(default=True, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    nome: str = Field(max_length=150, nullable=False)
    login: str = Field(max_length=80, unique=True, nullable=False)
    senha_hash: str = Field(max_length=255, nullable=False)
    perfil: PerfilUsuario = Field(default=PerfilUsuario.operador, nullable=False)
    ativo: bool = Field(default=True, nullable=False)
    ultimo_acesso: Optional[datetime] = Field(default=None)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Cliente(SQLModel, table=True):
    __tablename__ = "clientess"  # Ajustado com duplo 's' conforme o seu script SQL
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    nome: str = Field(max_length=150, nullable=False)
    tipo_pessoa: TipoPessoa = Field(default=TipoPessoa.fisica, nullable=False)
    documento: Optional[str] = Field(default=None, max_length=20)
    telefone: Optional[str] = Field(default=None, max_length=25)
    email: Optional[str] = Field(default=None, max_length=150)
    cep: Optional[str] = Field(default=None, max_length=10)
    endereco: Optional[str] = Field(default=None, max_length=200)
    numero: Optional[str] = Field(default=None, max_length=20)
    bairro: Optional[str] = Field(default=None, max_length=100)
    cidade: Optional[str] = Field(default=None, max_length=100)
    estado: Optional[str] = Field(default=None, max_length=2)
    observacoes: Optional[str] = Field(default=None)
    ativo: bool = Field(default=True, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    atualizado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Veiculo(SQLModel, table=True):
    __tablename__ = "veiculos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    cliente_id: Optional[int] = Field(default=None, foreign_key="clientess.id", nullable=True)
    placa: str = Field(max_length=10, nullable=False)
    marca: Optional[str] = Field(default=None, max_length=60)
    modelo: Optional[str] = Field(default=None, max_length=80)
    cor: Optional[str] = Field(default=None, max_length=40)
    ano: Optional[int] = Field(default=None)
    tipo: TipoVeiculo = Field(default=TipoVeiculo.carro, nullable=False)
    observacoes: Optional[str] = Field(default=None)
    ativo: bool = Field(default=True, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Vaga(SQLModel, table=True):
    __tablename__ = "vagas"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    identificacao: str = Field(max_length=20, nullable=False)
    setor: Optional[str] = Field(default=None, max_length=50)
    tipo: TipoVeiculo = Field(default=TipoVeiculo.carro, nullable=False)
    ativa: bool = Field(default=True, nullable=False)
    observacoes: Optional[str] = Field(default=None, max_length=255)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class TabelaPreco(SQLModel, table=True):
    __tablename__ = "tabelas_precos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    nome: str = Field(max_length=100, nullable=False)
    descricao: Optional[str] = Field(default=None, max_length=255)
    
    valor_hora: Decimal = Field(default=0.00, max_digits=10, decimal_places=2)
    valor_fracao: Decimal = Field(default=0.00, max_digits=10, decimal_places=2)
    minutos_fracao: int = Field(default=0)
    valor_diaria: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    valor_mensal: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    minutos_tolerancia: int = Field(default=0)
    
    cobrar_fracao: bool = Field(default=False, nullable=False)
    ativo: bool = Field(default=True, nullable=False)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    atualizado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class ContratoMensal(SQLModel, table=True):
    __tablename__ = "contratos_mensais"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    cliente_id: int = Field(foreign_key="clientess.id", nullable=False)
    veiculo_id: int = Field(foreign_key="veiculos.id", nullable=False)
    tabela_preco_id: int = Field(foreign_key="tabelas_precos.id", nullable=False)
    
    data_inicio: date = Field(nullable=False)
    data_fim: Optional[date] = Field(default=None)
    dia_vencimento: int = Field(nullable=False)
    valor_mensal: Decimal = Field(max_digits=10, decimal_places=2, nullable=False)
    
    status: StatusContrato = Field(default=StatusContrato.ativo, nullable=False)
    observacoes: Optional[str] = Field(default=None)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Movimentacao(SQLModel, table=True):
    __tablename__ = "movimentacoes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    veiculo_id: int = Field(foreign_key="veiculos.id", nullable=False)
    vaga_id: Optional[int] = Field(default=None, foreign_key="vagas.id", nullable=True)
    tabela_preco_id: int = Field(foreign_key="tabelas_precos.id", nullable=False)
    
    usuario_entrada_id: Optional[int] = Field(default=None, foreign_key="usuarios.id", nullable=True)
    usuario_saida_id: Optional[int] = Field(default=None, foreign_key="usuarios.id", nullable=True)
    
    entrada_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    saida_em: Optional[datetime] = Field(default=None)
    
    tipo_cobranca: TipoCobranca = Field(default=TipoCobranca.hora, nullable=False)
    
    valor_calculado: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    desconto: Decimal = Field(default=0.00, max_digits=10, decimal_places=2, nullable=False)
    valor_cobrado: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    
    status: StatusMovimentacao = Field(default=StatusMovimentacao.aberta, nullable=False)
    observacoes: Optional[str] = Field(default=None)
    criado_em: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class Pagamento(SQLModel, table=True):
    __tablename__ = "pagamentoss"  # Ajustado com duplo 's' conforme o seu script SQL
    
    id: Optional[int] = Field(default=None, primary_key=True)
    estacionamento_id: int = Field(foreign_key="estacionamentos.id", nullable=False)
    
    movimentacao_id: Optional[int] = Field(default=None, foreign_key="movimentacoes.id", nullable=True)
    contrato_mensal_id: Optional[int] = Field(default=None, foreign_key="contratos_mensais.id", nullable=True)
    
    valor: Decimal = Field(max_digits=10, decimal_places=2, nullable=False)
    forma_pagamento: FormaPagamento = Field(nullable=False)
    status: StatusPagamento = Field(default=StatusPagamento.pago, nullable=False)
    
