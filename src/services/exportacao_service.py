"""
Service para Exportação de uvas, vinhos e derivados
do Brasil.
"""

import logging
from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from src.repositories.exportacao_repository import ExportacaoRepository
from src.repositories.raw_repository import RawRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser
from src.config.logging_config import configurar_logging

logger = logging.getLogger(__name__)


class ExportacaoService:
    """
    Service para Exportação de uvas, vinhos e derivados
do Brasil.
    """

    def __init__(self):
        self._repo_raw = RawRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna a exportação de uvas, vinhos e derivados do Brasil por ano.
        """
        try:
            exportacao_raspagem = ExportacaoRaspagem(ano, "subopt_01")
            exportacao_raspagem.buscar_html()
            dados = exportacao_raspagem.parser_html()

            self._repo_raw.upsert(
                endpoint="exportacao",
                ano=ano,
                subopcao="subopt_01",
                payload=dados
            )

            self.exportacao_repository.salvar_ou_atualizar(dados, ano)

        except TimeoutRequisicao:
            logger.warning(f"[EXPORTACAO] Timeout ao acessar dados do ano {ano}. Retornando dados locais.")
        except ErroRequisicao as e:
            logger.warning(f"[EXPORTACAO] Erro HTTP {e.status_code} ao acessar dados de {ano}. Retornando dados locais.")
        except ErroParser as e:
            logger.error(f"[EXPORTACAO] Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception as e:
            logger.exception(f"[EXPORTACAO] Erro inesperado ao processar dados de {ano}: {e}")

        return self.exportacao_repository.get_por_ano(ano)
