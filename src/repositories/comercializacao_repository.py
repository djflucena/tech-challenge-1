"""Classe responsável por gerenciar os dados de comercialização"""
from src.config import BANCO_DE_DADOS


class ComercializacaoRepository:
    """
    Classe responsável por gerenciar os dados de comercialização
    """
    def get_por_ano(self, ano: int):
        """Retorna os dados de comercialização para o ano especificado."""
        try:
            return BANCO_DE_DADOS[ano]
        except KeyError as e:
            raise Exception(f"Dados não encontrados para o ano {ano}") from e

    def salvar_ou_atualizar(self, dados, ano):
        """Salva ou atualiza os dados no banco de dados."""
        BANCO_DE_DADOS[ano] = dados
