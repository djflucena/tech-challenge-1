"""
Service para Produção de vinhos, sucos e derivados
do Rio Grande do Sul.
"""

import logging
from src.raspagem.producao_raspagem import ProducaoRaspagem
from src.repositories.producao_repository import ProducaoRepository
from src.repositories.raw_repository import RawRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser
from src.config.logging_config import configurar_logging


logger = logging.getLogger(__name__)

class ProducaoService:
    """
    Service para Produção de vinhos, sucos e derivados
do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()
        self.producao_repository = ProducaoRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna a produção de vinhos, sucos e derivados
do Rio Grande do Sul por ano.
        """
        try:
            producao_raspagem = ProducaoRaspagem(ano)
            producao_raspagem.buscar_html()
            dados = producao_raspagem.parser_html()

            self._repo_raw.upsert(
                endpoint="producao",
                ano=ano,
                subopcao=None,
                payload=dados
            )

            self.producao_repository.salvar_ou_atualizar(dados, ano)

        except TimeoutRequisicao:
            logger.warning(f"[PRODUCAO] Timeout ao acessar dados do ano {ano}. Retornando dados locais.")
        except ErroRequisicao as e:
            logger.warning(f"[PRODUCAO] Erro HTTP {e.status_code} ao acessar dados de {ano}. Retornando dados locais.")
        except ErroParser as e:
            logger.error(f"[PRODUCAO] Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception as e:
            logger.exception(f"[PRODUCAO] Erro inesperado ao processar dados de {ano}: {e}")

        return self.producao_repository.get_por_ano(ano)
