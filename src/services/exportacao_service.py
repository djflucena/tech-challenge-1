"""Service para exportação de vinhos, sucos e derivados
    do Rio Grande do Sul."""
from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from src.repositories.raw_repository import RawRepository

class ExportacaoService:
    """Service para exportação de vinhos, sucos e derivados
    do Rio Grande do Sul."""

    def __init__(self):
        self._repo_raw = RawRepository()

    def get_por_ano(self, ano: int, subopcao: str):
        """
        Retorna a exportação de vinhos, sucos e derivados
        Tenta raspar; em falha, retorna o que estiver salvo.
        """
        try:
            exportacao_raspagem = ExportacaoRaspagem(ano, subopcao)
            exportacao_raspagem.buscar_html()
            dados = exportacao_raspagem.parser_html()

            if dados:
                self._repo_raw.upsert(
                    endpoint="exportacao",
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
            endpoint="exportacao",
            ano=ano,
            subopcao=subopcao
        )
        return {"source": "banco", "data": dados_banco}
