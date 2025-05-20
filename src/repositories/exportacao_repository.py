# src/repositories/exportacao.py
"""Classe responsável por gerenciar os dados de exportação"""
from src.repositories.raw_repository import RawRepository

class ExportacaoRepository(RawRepository):
    """
    Classe responsável por gerenciar os dados de exportação.
    Exige subopcao
    """
    def __init__(self):
        super().__init__(categoria="exportacao", has_subopcao=True)
