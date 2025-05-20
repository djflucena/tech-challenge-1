# src/repositories/importacao.py
"""Classe responsável por gerenciar os dados de importação"""
from src.repositories.raw_repository import RawRepository

class ImportacaoRepository(RawRepository):
    """
    Classe responsável por gerenciar os dados de importação.
    Exige subopcao
    """
    def __init__(self):
        super().__init__(categoria="importacao", has_subopcao=True)
