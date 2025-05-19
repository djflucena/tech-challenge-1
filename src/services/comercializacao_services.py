"""
Service para Comercialização de vinhos, sucos e derivados
do Rio Grande do Sul.
"""

import logging
from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem
from src.repositories.raw_repository import RawRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser
from src.config.logging_config import configurar_logging

logger = logging.getLogger(__name__)


class ComercializacaoService:
    """
    Service para Comercialização de vinhos, sucos e derivados
do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna a comercialização de vinhos, sucos e derivados
do Rio Grande do Sul por ano.
        """
        try:
            comercializacao_raspagem = ComercializacoRaspagem(ano)
            comercializacao_raspagem.buscar_html()
            dados = comercializacao_raspagem.parser_html()

            self._repo_raw.upsert(
                endpoint="comercializacao",
                ano=ano,
                subopcao=None,
                payload=dados
            )

            self.comercializacao_repository.salvar_ou_atualizar(dados, ano)

        except TimeoutRequisicao:
            logger.warning(f"[COMERCIALIZACAO] Timeout ao acessar dados do ano {ano}. Retornando dados locais.")
        except ErroRequisicao as e:
            logger.warning(f"[COMERCIALIZACAO] Erro HTTP {e.status_code} ao acessar dados de {ano}. Retornando dados locais.")
        except ErroParser as e:
            logger.error(f"[COMERCIALIZACAO] Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception as e:
            logger.exception(f"[COMERCIALIZACAO] Erro inesperado ao processar dados de {ano}: {e}")

        return self.comercializacao_repository.get_por_ano(ano)
