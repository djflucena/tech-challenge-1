from src.scrapping_service import RaspagemService
from src.repositories import ProducaoRepository

class ProducaoService:
    """
        Service para Produção de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    def __init__(self):
        self.producao_repository = ProducaoRepository()
        self.scrapping_service = RaspagemService("https://www.example.com")

    def get_por_ano(self, ano: int):
        """
            Retorna a produção de vinhos, sucos e derivados do Rio Grande do Sul por ano.
        """
        try:
            self.scrapping_service.buscar_dados()
            dados = self.scrapping_service.converter_dados()
            self.producao_repository.salvar(dados)
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
        return self.producao_repository.get_por_ano(ano)

