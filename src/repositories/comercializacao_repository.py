# src/repositories/comercializacao.py
"""Classe responsável por gerenciar os dados de comercialização"""
from src.repositories.raw_repository import RawRepository

class ComercializacaoRepository(RawRepository):
    """
    Classe responsável por gerenciar os dados de comercialização.
    NÃO exige subopcao.
    """
    def __init__(self):
        super().__init__(categoria="comercializacao", has_subopcao=False)
