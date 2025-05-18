"""
Service para Importação de uvas, vinhos e derivados
do Brasil.
"""

import logging
from src.raspagem.importacao_raspagem import ImportacaoRaspagem
from src.repositories.importacao_repository import ImportacaoRepository
from src.repositories.raw_repository import RawRepository
from src.raspagem.raspagem_exceptions import ErroRequisicao, TimeoutRequisicao, ErroParser


class ImportacaoService:
    """
    Service para Importação de uvas, vinhos e derivados
do Brasil.
    """

    def __init__(self):
        self._repo_raw = RawRepository()
        self.importacao_repository = ImportacaoRepository()

    def get_por_ano(self, ano: int):
        """
        Retorna a importação de uvas, vinhos e derivados do Brasil por ano.
        """
        try:
            importacao_raspagem = ImportacaoRaspagem(ano, "subopt_01")
            importacao_raspagem.buscar_html()
            dados = importacao_raspagem.parser_html()

            self._repo_raw.upsert(
                endpoint="importacao",
                ano=ano,
                subopcao="subopt_01",
                payload=dados
            )

            self.importacao_repository.salvar_ou_atualizar(dados, ano)

        except TimeoutRequisicao:
            logging.warning(f"[IMPORTACAO] Timeout ao acessar dados do ano {ano}. Retornando dados locais.")
        except ErroRequisicao as e:
            logging.warning(f"[IMPORTACAO] Erro HTTP {e.status_code} ao acessar dados de {ano}. Retornando dados locais.")
        except ErroParser as e:
            logging.error(f"[IMPORTACAO] Falha ao interpretar HTML do ano {ano}: {e}")
        except Exception as e:
            logging.exception(f"[IMPORTACAO] Erro inesperado ao processar dados de {ano}: {e}")

        return self.importacao_repository.get_por_ano(ano)
