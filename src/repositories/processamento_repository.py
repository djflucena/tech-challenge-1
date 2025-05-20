# src/repositories/processamento.py
"""Classe responsável por gerenciar os dados de processamento"""
from src.repositories.raw_repository import RawRepository

class ProcessamentoRepository(RawRepository):
    """
    Classe responsável por gerenciar os dados de processamento.
    Exige subopcao
    """
    def __init__(self):
        super().__init__(categoria="processamento", has_subopcao=True)
