"""Classe responsável por gerenciar os dados de processamento"""
# src/repositories/processamento.py
from src.repositories.base import BaseRepository

class ProcessamentoRepository(BaseRepository):
    """
    Classe responsável por gerenciar os dados de processamento
    de uvas viníferas, americanas, de mesa e sem classificação.
    """
    def __init__(self):
        # “processamento” é a chave em src/config.py e exige subopcao
        super().__init__(categoria="processamento", has_subopcao=True)
