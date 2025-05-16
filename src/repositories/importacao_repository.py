"""Classe responsável por gerenciar os dados de importação"""
from src.config import BANCO_DE_DADOS


class ImportacaoRepository:
    """
    Classe responsável por gerenciar os dados de importação"""

    def get_opcao_por_ano(self, ano: int, subopcao: str):
        """Retorna os dados de importação para o ano e subopção especificados."""
        return BANCO_DE_DADOS[ano][subopcao]

    def salvar_ou_atualizar(self, dados, ano, subopcao):
        """Salva ou atualiza os dados no banco de dados."""
        if ano not in BANCO_DE_DADOS:
            BANCO_DE_DADOS[ano] = {}
        if subopcao not in BANCO_DE_DADOS[ano]:
            BANCO_DE_DADOS[ano][subopcao] = {}
        BANCO_DE_DADOS[ano][subopcao] = dados
