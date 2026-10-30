import os
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv

load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")

class EstacionamentoService:
    @staticmethod
    def buscar_veiculos(estacionamento_id: int) -> List[Dict]:
        """
        Consome o endpoint do FastAPI para listar todos os veículos de um estacionamento.
        """
        try:
            url = f"{FASTAPI_URL}/veiculos/{estacionamento_id}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def buscar_movimentacoes_ativas(estacionamento_id: int) -> List[Dict]:
        """
        Consome as movimentações. Como criamos a dependência por cabeçalho no FastAPI,
        enviamos o X-Estacionamento-ID no Header da requisição.
        """
        try:
            # Caso sua rota do FastAPI use filtros, fazemos a chamada passando o Header obrigatório
            url = f"{FASTAPI_URL}/movimentacoes/entrada" 
            headers = {"X-Estacionamento-ID": str(estacionamento_id)}
            
            # Nota: Como o FastAPI retorna uma lista com base nos filtros do banco,
            # fazemos o GET enviando os cabeçalhos de segurança mapeados na pasta dependencies.
            response = requests.get(f"{FASTAPI_URL}/movimentacoes/", headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def registrar_entrada_veiculo(estacionamento_id: int, veiculo_id: int, tabela_preco_id: int) -> Optional[Dict]:
        """
        Envia uma requisição POST ao FastAPI para realizar o check-in de um veículo.
        """
        try:
            url = f"{FASTAPI_URL}/movimentacoes/entrada"
            payload = {
                "estacionamento_id": estacionamento_id,
                "veiculo_id": veiculo_id,
                "tabela_preco_id": tabela_preco_id,
                "status": "aberta"
            }
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 201:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None
