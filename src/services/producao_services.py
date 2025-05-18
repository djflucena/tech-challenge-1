""" Service para Produção de vinhos, sucos e derivados
do Rio Grande do Sul. """
from src.raspagem.producao_raspagem import ProducaoRaspagem
from src.repositories.raw_repository import RawRepository

class ProducaoService:
    """
    Service para Produção de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna a produção de vinhos, sucos e derivados
        do Rio Grande do Sul por ano.
        Tenta raspar; em falha, retorna o que estiver salvo.
        """
        try:
            producao_raspagem = ProducaoRaspagem(ano)
            producao_raspagem.buscar_html()
            dados = producao_raspagem.parser_html()
  
            if dados:
                self._repo_raw.upsert(
                    endpoint="producao",
                    ano=ano,
                    subopcao=None,
                    payload=dados
                )
                return {"source": "site", "data": dados}

        except Exception:
            pass

        """
        Fallback: busca no banco
        """
        dados_banco = self._repo_raw.get(
            endpoint="producao",
            ano=ano,
            subopcao=None
        )
        return {"source": "banco", "data": dados_banco}
