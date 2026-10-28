from sqlmodel import create_engine
from app.config import settings

# Criação da Engine com configurações robustas para ambiente compartilhado/produção
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,              # Mude para True em ambiente de testes para ver os SQLs no console
    pool_recycle=1800,       # Evita o erro 'MySQL server has gone away' reciclando conexões a cada 30 min
    pool_pre_ping=True,      # Testa a saúde da conexão antes de executar qualquer query
    pool_size=10,            # Quantidade de conexões mantidas ativas simultaneamente
    max_overflow=20          # Limite de conexões extras que podem ser abertas sob alta demanda
)
