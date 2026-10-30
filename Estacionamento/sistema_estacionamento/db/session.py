from sqlmodel import Session
from typing import Generator
from app.db.connection import engine

def get_session() -> Generator[Session, None, None]:
    """
    Dependência injetável do FastAPI. Abre uma sessão limpa por requisição
    e garante o fechamento automático no final, mesmo em caso de erro.
    """
    with Session(engine) as session:
        yield session
