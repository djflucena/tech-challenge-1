# src/services/comercializacao_service.py
"""Service para comercialização de vinhos, sucos e derivados
do Rio Grande do Sul."""

import logging
from datetime import datetime, timezone
from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem
from src.repositories.comercializacao_repository import ComercializacaoRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser
from src.config.logging_config import configurar_logging

configurar_logging()
logger = logging.getLogger(__name__)

class ComercializacaoService:
    """
    Service para Comercialização de vinhos, sucos e derivados
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

        except TimeoutRequisicao:
            logger.warning(f"Timeout ao acessar dados do ano {ano}; usando dados locais.")
        except ErroRequisicao as e:
            logger.warning(f"Erro HTTP {e.status_code} ao acessar ano {ano}; usando dados locais.")
        except ErroParser as e:
            logger.error(f"Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception:
            logger.exception(f"Erro inesperado ao processar dados de {ano}; usando dados locais.")

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
