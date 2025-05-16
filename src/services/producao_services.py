"""
Service para Produção de vinhos, sucos e derivados
do Rio Grande do Sul.
"""

from src.raspagem.producao_raspagem import ProducaoRaspagem
from src.repositories.producao_repository import ProducaoRepository


class ProducaoService:
    """
    Service para Produção de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self.producao_repository = ProducaoRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna a produção de vinhos, sucos e derivados
        do Rio Grande do Sul por ano.
        """
        try:
            producao_raspagem = ProducaoRaspagem(ano)
            producao_raspagem.buscar_html()
            dados = producao_raspagem.parser_html()

            self.producao_repository.salvar_ou_atualizar(dados, ano)
        except Exception:
            print("Erro ao buscar dados")
        return self.producao_repository.get_por_ano(ano)
