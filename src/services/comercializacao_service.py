# src/services/comercializacao_service.py
"""Service para comercialização de vinhos, sucos e derivados
do Rio Grande do Sul."""
from datetime import datetime, timezone
from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem
from src.repositories.comercializacao_repository import ComercializacaoRepository

class ComercializacaoService:
    """
    Service para comercialização de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo = ComercializacaoRepository()

    def get_por_ano(self, ano: int) -> dict:
        """
        Retorna a comercialização de vinhos, sucos e derivados.
        Tenta raspar; em falha, retorna o que estiver salvo.
        Sempre com as chaves 'source', 'fetched_at' e 'data'.
        """
        try:
            raspagem = ComercializacoRaspagem(ano)
            raspagem.buscar_html()
            dados = raspagem.parser_html()
            agora = datetime.now(timezone.utc)

            if dados:
                self._repo.salvar_ou_atualizar(dados, ano)
                return {
                    "source":     "site",
                    "fetched_at": agora,
                    "data":       dados
                }

        except Exception as e:
            print(f"[warn] erro na raspagem: {e}")

        registro = self._repo.get_por_ano(ano)
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