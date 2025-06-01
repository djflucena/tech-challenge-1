import logging
from abc import ABC, abstractmethod 
from datetime import datetime, timezone

from src.raspagem.base_raspagem import BaseRaspagem
from src.raspagem.raspagem_exceptions import ErroParser, ErroRequisicao, TimeoutRequisicao
from src.repositories.raw_repository import RawRepository
from src.repositories.exceptions import ErroConexaoBD, ErroConsultaBD, RegistroNaoEncontrado
from src.schemas.base_schema import BaseResponse


class BaseService(ABC):

    def __init__(self, repository: RawRepository):
        self.logger = logging.getLogger(self.__class__.__module__)
        self.repository = repository

    
    def get_por_ano(self, ano: int, subopcao: str | None = None) -> BaseResponse:
        dados = None
        agora = None

        try:
            raspagem = self.get_raspagem(ano, subopcao)
            raspagem.buscar_html()
            dados = raspagem.parser_html()
            agora = datetime.now(timezone.utc)

            try:
                self.repository.salvar_ou_atualizar(dados, ano, subopcao)
            except (ErroConexaoBD, ErroConsultaBD) as e:
                self.logger.warning(
                    f'[Cache/DB] Falha ao salvar/atualizar os dados no banco: {e}.'
                    f' Dados continuarão sendo utilizados a partir da raspagem (site).'
                )
        
            return self.get_reponse(source = 'site', fetched_at = agora, data = dados)

        except Exception as e:
            self._log_exception(e, ano)

            try:
                registro = self.repository.get_por_ano(ano, subopcao)
                if registro:
                    return self.get_reponse(source = 'banco',
                                            fetched_at = registro['fetched_at'],
                                            data = registro['data'])

            except RegistroNaoEncontrado as e:
                self.logger.warning(
                    f'[Fallback] Falha ao obter dados de {ano}: nenhuma resposta do site e cache '
                    f' inexistente no banco de dados.')

            except (ErroConexaoBD, ErroConsultaBD) as e:
                self.logger.error(f'[Cache/DB] Falha ao salvar/atualizar os dados no banco: {e}.')
                raise e


    @abstractmethod
    def get_raspagem(self, ano: int, subopcao: str) -> BaseRaspagem:
        pass


    @abstractmethod
    def get_reponse(self, source: str, fetched_at: datetime, data: dict) -> BaseResponse:
        pass
        

    def _log_exception(self, e, ano):
        if isinstance(e, TimeoutRequisicao):
            self.logger.warning(
                f'[Requisição] Timeout ao tentar obter dados de {ano} via site.' 
                f' Utilizando fallback do banco de dados.'
            )

        elif isinstance(e, ErroRequisicao):
            self.logger.warning(
                f'[Requisição] Erro HTTP {e.status_code} ao acessar dados de {ano}.' 
                f' Utilizando fallback do banco de dados.'
            )
        
        elif isinstance(e, ErroParser):
            self.logger.error(f'[Parser] Erro ao interpretar HTML para o ano {ano}: {e}.')
        
        else:
            self.logger.exception(
                f'[Erro] Erro inesperado durante o processamento de dados do ano {ano}.' 
                f' Utilizando fallback para o banco de dados.'
            )
