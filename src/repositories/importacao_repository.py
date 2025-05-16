"""Classe responsável por gerenciar os dados de importação"""
# src/repositories/importacao.py
from src.repositories.base import BaseRepository

class ImportacaoRepository(BaseRepository):
    """
    Classe responsável por gerenciar os dados de importação.
    """
    def __init__(self):
        # “importacao” é a chave em src/config.py e exige subopcao
        super().__init__(categoria="importacao", has_subopcao=True)
