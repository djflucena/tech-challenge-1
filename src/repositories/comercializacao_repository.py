"""Classe responsável por gerenciar os dados de comercialização"""
# src/repositories/comercializacao.py
from src.repositories.base import BaseRepository

class ComercializacaoRepository(BaseRepository):
    """
    Classe responsável por gerenciar os dados de comercialização.
    """
    def __init__(self):
        # “comercializacao” é a chave em src/config.py e NÃO exige subopcao
        super().__init__(categoria="comercializacao", has_subopcao=False)
