# src/services/processamento_service.py
"""
Service para processamento de vinhos, sucos e derivados
do Rio Grande do Sul.
"""

import logging
from datetime import datetime, timezone
from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from src.repositories.processamento_repository import ProcessamentoRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser
from src.repositories.exceptions import (
    ErroConexaoBD,
    ErroConsultaBD,
    RegistroNaoEncontrado,
)
from src.config.logging_config import configurar_logging

configurar_logging()
logger = logging.getLogger(__name__)

class ProcessamentoService:
    """
    Service para Processamento de uvas
    do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo = ProcessamentoRepository()

    def get_por_ano(self, ano: int, subopcao: str) -> dict:
        """
        Retorna a processamento de uvas.
        Tenta raspar; em falha, retorna o que estiver salvo.
        Sempre com as chaves 'source', 'fetched_at' e 'data'.
        """
        try:
            raspagem = ProcessamentoRaspagem(ano, subopcao)
            raspagem.buscar_html()
            dados = raspagem.parser_html()
            agora = datetime.now(timezone.utc)

        except TimeoutRequisicao:
            logger.warning(f"Timeout ao acessar dados do ano {ano}; usando dados locais.")
        except ErroRequisicao as e:
            logger.warning(f"Erro HTTP {e.status_code} ao acessar ano {ano}; usando dados locais.")
        except ErroParser as e:
            logger.error(f"Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception:
            logger.exception(f"Erro inesperado ao processar dados de {ano}; usando dados locais.")

        if dados:
            try:
                self._repo.salvar_ou_atualizar(dados, ano, subopcao)
            except (ErroConexaoBD, ErroConsultaBD) as e:
                logger.warning(f"Impossível salvar cache: {e}; continuando com dados do site.")

            return {
                "source":     "site",
                "fetched_at": agora,
                "data":       dados
            }

        try:
            registro = self._repo.get_por_ano(ano, subopcao)
        except RegistroNaoEncontrado:
            logger.warning(f"Sem dados no site nem no banco para o ano {ano}.")
            return {
                "source":     "banco",
                "fetched_at": None,
                "data":       None
            }
        except (ErroConexaoBD, ErroConsultaBD) as e:
            logger.error(f"Erro de persistência: {e}")
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