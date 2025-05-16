"""Classe responsável por gerenciar os dados de exportação"""
# src/repositories/exportacao.py
from src.repositories.base import BaseRepository

class ExportacaoRepository(BaseRepository):
    """
    Classe responsável por gerenciar os dados de exportação.
    """
    def __init__(self):
        # “exportacao” é a chave em src/config.py e exige subopcao
        super().__init__(categoria="exportacao", has_subopcao=True)
