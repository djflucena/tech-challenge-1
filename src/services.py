from src.repositories import ProducaoRepository

class ProducaoService:
    """
        Service para Produção de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    def __init__(self):
        self.producao_repository = ProducaoRepository()

    def get_por_ano(self, ano: int):
        """
            Retorna a produção de vinhos, sucos e derivados do Rio Grande do Sul por ano.
        """
        return self.producao_repository.get_por_ano(ano)

