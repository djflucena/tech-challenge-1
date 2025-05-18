"""Service para processamento de vinhos, sucos e derivados
    do Rio Grande do Sul."""
from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from src.repositories.raw_repository import RawRepository

class ProcessamentoService:
    """
    Service para processamento de uvas viníferas, americanas,
    de mesa e sem classificação no Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()

    def get_por_ano(self, ano: int, subopcao: str):
        """
        Retorna a processamento de uvas.
        Tenta raspar; em falha, retorna o que estiver salvo.
        """
        try:
            raspagem = ProcessamentoRaspagem(ano, subopcao)
            raspagem.buscar_html()
            dados = raspagem.parser_html()
  
            if dados:
                self._repo_raw.upsert(
                    endpoint="processamento",
                    ano=ano,
                    subopcao=subopcao,
                    payload=dados
                )
                return {"source": "site", "data": dados}

        except Exception:
            pass
        """
        Fallback: busca no banco
        """
        dados_banco = self._repo_raw.get(
            endpoint="processamento",
            ano=ano,
            subopcao=subopcao
        )
        return {"source": "banco", "data": dados_banco}
