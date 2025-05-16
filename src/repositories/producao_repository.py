"""
    Classe responsável por gerenciar os dados de produção
"""
# src/repositories/producao.py
from src.repositories.base import BaseRepository

class ProducaoRepository(BaseRepository):
    """
    Classe responsável por gerenciar os dados de produção.
    """
    def __init__(self):
        # “producao” é a chave em src/config.py e NÃO exige subopcao
        super().__init__(categoria="producao", has_subopcao=False)
