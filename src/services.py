from src.raspagem_service import ProducaoRaspagem
from src.repositories import ProducaoRepository

class ProducaoService:
    """
        Service para Produção de vinhos, sucos e derivados 
        do Rio Grande do Sul.
    """
    def __init__(self):
        self.producao_repository = ProducaoRepository()
        self.producao_raspagem = ProducaoRaspagem()

    def get_por_ano(self, ano: int):
        """
            Retorna a produção de vinhos, sucos e derivados 
            do Rio Grande do Sul por ano.
        """
        try:
            self.producao_raspagem.buscar_html(ano)
            dados = self.producao_raspagem.converter_dados()
            self.producao_repository.salvar(dados)
        except Exception as e:
            print(f"Erro ao buscar dados: {e}")
        return self.producao_repository.get_por_ano(ano)

