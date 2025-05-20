# src/services/exportacao_service.py
"""Service para exportação de vinhos, sucos e derivados
    do Rio Grande do Sul."""
from datetime import datetime, timezone
from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from src.repositories.exportacao_repository import ExportacaoRepository

class ExportacaoService:
    """
    Service para exportação de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo = ExportacaoRepository()

    def get_por_ano(self, ano: int, subopcao: str) -> dict:
        """
        Retorna a exportação de vinhos, sucos e derivados
        Tenta raspar; em falha, retorna o que estiver salvo.
        Sempre com as chaves 'source', 'fetched_at' e 'data'.
        """
        try:
            exportacao_raspagem = ExportacaoRaspagem(ano, subopcao)
            exportacao_raspagem.buscar_html()
            dados = exportacao_raspagem.parser_html()
            agora = datetime.now(timezone.utc)

            if dados:
                self._repo.salvar_ou_atualizar(dados, ano, subopcao)
                return {
                    "source":     "site",
                    "fetched_at": agora,
                    "data":       dados
                }

        except Exception as e:
            print(f"[warn] erro na raspagem: {e}")
            
        registro = self._repo.get_por_ano(ano, subopcao)
        if registro is None:
            return {
                "source":     "banco",
                "fetched_at": None,
                "data":       None
            }

        return {
            "source":     "banco",
            "fetched_at": registro["fetched_at"],
            "data":       registro["data"]
        }