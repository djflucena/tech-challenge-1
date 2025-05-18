"""
Service para Processamento de uvas
do Rio Grande do Sul.
"""

import logging
from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from src.repositories.processamento_repository import ProcessamentoRepository
from src.repositories.raw_repository import RawRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser


class ProcessamentoService:
    """
    Service para Processamento de uvas
do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()
        self.processamento_repository = ProcessamentoRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna o processamento de uvas do Rio Grande do Sul por ano.
        """
        try:
            processamento_raspagem = ProcessamentoRaspagem(ano, "subopt_01")
            processamento_raspagem.buscar_html()
            dados = processamento_raspagem.parser_html()

            self._repo_raw.upsert(
                endpoint="processamento",
                ano=ano,
                subopcao="subopt_01",
                payload=dados
            )

            self.processamento_repository.salvar_ou_atualizar(dados, ano)

        except TimeoutRequisicao:
            logging.warning(f"[PROCESSAMENTO] Timeout ao acessar dados do ano {ano}. Retornando dados locais.")
        except ErroRequisicao as e:
            logging.warning(f"[PROCESSAMENTO] Erro HTTP {e.status_code} ao acessar dados de {ano}. Retornando dados locais.")
        except ErroParser as e:
            logging.error(f"[PROCESSAMENTO] Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception as e:
            logging.exception(f"[PROCESSAMENTO] Erro inesperado ao processar dados de {ano}: {e}")

        return self.processamento_repository.get_por_ano(ano)
