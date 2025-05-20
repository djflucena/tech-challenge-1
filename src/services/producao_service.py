# src/services/producao_service.py
"""
Service para Produção de vinhos, sucos e derivados
do Rio Grande do Sul.
"""

import logging
from datetime import datetime, timezone
from src.config.logging_config import configurar_logging
from src.raspagem.producao_raspagem import ProducaoRaspagem
from src.repositories.producao_repository import ProducaoRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser

configurar_logging()
logger = logging.getLogger(__name__)

class ProducaoService:
    """
    Service para produção de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo = ProducaoRepository()

    def get_por_ano(self, ano: int) -> dict:
        """
        Retorna a produção de vinhos, sucos e derivados.
        Tenta raspar; em falha ou sem dados, retorna o que estiver salvo,
        sempre com as chaves 'source', 'fetched_at' e 'data'.
        """
        try:
            raspagem = ProducaoRaspagem(ano)
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
