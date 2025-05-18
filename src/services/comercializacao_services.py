"""Service para comercialização de vinhos, sucos e derivados
do Rio Grande do Sul."""
from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem
from src.repositories.raw_repository import RawRepository

class ComercializacaoService:
    """
    Service para comercialização de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna a comercialização de vinhos, sucos e derivados
        do Rio Grande do Sul por ano.
        Tenta raspar; em falha, retorna o que estiver salvo.
        """
        try:
            comercializacao_raspagem = ComercializacoRaspagem(ano)
            comercializacao_raspagem.buscar_html()
            dados = comercializacao_raspagem.parser_html()

            if dados:
                self._repo_raw.upsert(
                    endpoint="comercializacao",
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
            endpoint="comercializacao",
            ano=ano,
            subopcao=None
        )
        return {"source": "banco", "data": dados_banco}
