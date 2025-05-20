# src/services/importacao_service.py
"""Service para importação de vinhos, sucos e derivados
    do Rio Grande do Sul."""
from datetime import datetime, timezone
from src.raspagem.importacao_raspagem import ImportacaoRaspagem
from src.repositories.importacao_repository import ImportacaoRepository

class ImportacaoService:
    """
    Service para importação de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo = ImportacaoRepository()

    def get_por_ano(self, ano: int, subopcao: str) -> dict:
        """
        Retorna a importação de vinhos, sucos e derivados
        Tenta raspar; em falha, retorna o que estiver salvo.
        Sempre com as chaves 'source', 'fetched_at' e 'data'.
        """
        try:
            importacao_raspagem = ImportacaoRaspagem(ano, subopcao)
            importacao_raspagem.buscar_html()
            dados = importacao_raspagem.parser_html()
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