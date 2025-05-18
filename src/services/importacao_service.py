"""Service para importação de vinhos, sucos e derivados
    do Rio Grande do Sul."""
from src.raspagem.importacao_raspagem import ImportacaoRaspagem
from src.repositories.raw_repository import RawRepository

class ImportacaoService:
    """Service para importação de vinhos, sucos e derivados
    do Rio Grande do Sul."""

    def __init__(self):
        self._repo_raw = RawRepository()

    def get_por_ano(self, ano: int, subopcao: str):
        """
        Retorna a importação de vinhos, sucos e derivados
        Tenta raspar; em falha, retorna o que estiver salvo.
        """
        try:
            importacao_raspagem = ImportacaoRaspagem(ano, subopcao)
            importacao_raspagem.buscar_html()
            dados = importacao_raspagem.parser_html()
  
            if dados:
                self._repo_raw.upsert(
                    endpoint="importacao",
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
            endpoint="importacao",
            ano=ano,
            subopcao=subopcao
        )
        return {"source": "banco", "data": dados_banco}
