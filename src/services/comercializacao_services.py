"""
Service para Comercialização de vinhos, sucos e derivados
do Rio Grande do Sul.
"""

import logging
from src.raspagem.comercializacao_raspagem import ComercializacoRaspagem
from src.repositories.comercializacao_repository import ComercializacaoRepository
from src.repositories.raw_repository import RawRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser


class ComercializacaoService:
    """
    Service para Comercialização de vinhos, sucos e derivados
do Rio Grande do Sul.
    """

    def __init__(self):
        self._repo_raw = RawRepository()
        self.comercializacao_repository = ComercializacaoRepository()

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
            logging.warning(f"[COMERCIALIZACAO] Timeout ao acessar dados do ano {ano}. Retornando dados locais.")
        except ErroRequisicao as e:
            logging.warning(f"[COMERCIALIZACAO] Erro HTTP {e.status_code} ao acessar dados de {ano}. Retornando dados locais.")
        except ErroParser as e:
            logging.error(f"[COMERCIALIZACAO] Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception as e:
            logging.exception(f"[COMERCIALIZACAO] Erro inesperado ao processar dados de {ano}: {e}")

        return self.comercializacao_repository.get_por_ano(ano)
