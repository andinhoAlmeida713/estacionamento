import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Configurações do Aplicativo
    SECRET_KEY: str
    ENVIRONMENT: str = "development"
    
    # Configurações de Integração (Flask <-> FastAPI)
    FASTAPI_URL: str = "http://127.0.0.1:8000"
    FLASK_PORT: int = 5000
    FASTAPI_PORT: int = 8000

    # Configurações do Banco de Dados MySQL (Padrão para o ambiente aluno25)
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str = "aluno25"

    @property
    def DATABASE_URL(self) -> str:
        """Monta dinamicamente a string de conexão para o SQLAlchemy/SQLModel"""
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Carrega automaticamente o arquivo .env da raiz do projeto
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding="utf-8",
        extra="ignore" # Ignora outras variáveis que possam estar no .env
    )

# Instância global para ser importada em qualquer parte do sistema
settings = Settings()
