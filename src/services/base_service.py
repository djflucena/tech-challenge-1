from abc import ABC, abstractmethod 
from datetime import datetime, timezone
from typing import Any, Generic, Type, TypeVar

from src.raspagem.raspagem_exceptions import ErroParser, ErroRequisicao, TimeoutRequisicao
from src.repositories.exceptions import ErroConexaoBD, ErroConsultaBD, RegistroNaoEncontrado
from src.schemas.base_schema import BaseResponse


T = TypeVar("T", bound=BaseResponse)


class BaseService(ABC, Generic[T]):

    def __init__(self, response_cls: Type[T], raspagem_cls: Any, repository: Any, logger: Any):
        self.response_cls = response_cls
        self.raspagem_cls = raspagem_cls
        self.repository = repository
        self.logger = logger

    
    def get_por_ano(self, ano: int, subopcao: str | None = None) -> T:
        dados = None
        agora = None

        try:
            raspagem = self.raspagem_cls(ano, subopcao)
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

            return self.response_cls(
                source = 'site',
                fetched_at = agora,
                data = self._transformar_json_para_modelo(dados)
            )

        except Exception as e:
            self._log_exception(e, ano)

            try:
                registro = self.repository.get_por_ano(ano, subopcao)
                if registro:
                    return self.response_cls(
                        source = 'banco',
                        fetched_at = registro['fetched_at'],
                        data = self._transformar_json_para_modelo(registro['data'])
                    )

            except RegistroNaoEncontrado as e:
                self.logger.warning(
                    f'[Fallback] Falha ao obter dados de {ano}: nenhuma resposta do site e cache '
                    f' inexistente no banco de dados.')

            except (ErroConexaoBD, ErroConsultaBD) as e:
                self.logger.error(f'[Cache/DB] Falha ao salvar/atualizar os dados no banco: {e}.')
                raise e


    @abstractmethod
    def _transformar_json_para_modelo(data: dict) -> Any:
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
