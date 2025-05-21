# src/services/comercializacao_service.py
"""
Service para comercialização de vinhos, sucos e derivados
do Rio Grande do Sul.
"""

import logging
from datetime import datetime, timezone
from src.raspagem.comercializacao_raspagem import ComercializacaoRaspagem
from src.repositories.comercializacao_repository import ComercializacaoRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser
from src.repositories.exceptions import (
    ErroConexaoBD,
    ErroConsultaBD,
    RegistroNaoEncontrado,
)
from src.config.logging_config import configurar_logging

configurar_logging()
logger = logging.getLogger(__name__)

class ComercializacaoService:
    """
    Service para comercialização de vinhos, sucos e derivados
    do Rio Grande do Sul.
    """

    def __init__(self):
        self.comercializacao_repository = ComercializacaoRepository()

    def get_por_ano(self, ano: int) -> dict | str | None:
        """
        Retorna a comercialização de vinhos, sucos e derivados.
        Tenta raspar; em falha, retorna o que estiver salvo.
        Sempre com as chaves 'source', 'fetched_at' e 'data'.
        """
        dados = None
        agora = None

        try:
            raspagem = ComercializacaoRaspagem(ano)
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
                self.comercializacao_repository.salvar_ou_atualizar(dados, ano)
            except (ErroConexaoBD, ErroConsultaBD) as e:
                logger.warning(f"Impossível salvar cache: {e}; continuando com dados do site.")

            return {
                "source":     "site",
                "fetched_at": agora,
                "data":       dados
            }

        try:
            registro = self.comercializacao_repository.get_por_ano(ano)
        except RegistroNaoEncontrado:
            logger.warning(f"Sem dados no site nem no banco para o ano {ano}.")
            return {
                "source":     "api",
                "fetched_at": None,
                "data":       None
            }
        except (ErroConexaoBD, ErroConsultaBD) as e:
            logger.error(f"Erro de persistência: {e}")
            return {
                "source":     "api",
                "fetched_at": None,
                "data":       None
            }
        
        if not isinstance(registro, dict):
            return registro
        
        return {
            "source":     "banco",
            "fetched_at": registro["fetched_at"],
            "data":       registro["data"]
        }