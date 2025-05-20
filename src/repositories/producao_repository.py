# src/repositories/producao.py
"""Classe responsável por gerenciar os dados de produção"""
from src.repositories.raw_repository import RawRepository

class ProducaoRepository(RawRepository):
    """
    Classe responsável por gerenciar os dados de produção.
    NÃO exige subopcao
    """
    def __init__(self):
        super().__init__(categoria="producao", has_subopcao=False)
