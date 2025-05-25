import logging

from src.config.logging_config import configurar_logging
from src.raspagem.importacao_raspagem import ImportacaoRaspagem
from src.repositories.importacao_repository import ImportacaoRepository
from src.schemas.importacao_schema import Importacao, ImportacaoResponse
from src.services.base_service import BaseService


configurar_logging()
logger = logging.getLogger(__name__)


class ImportacaoService(BaseService[ImportacaoResponse]):
    """
    Service para importação de vinhos, sucos e derivados do Rio Grande do Sul.
    """

    def __init__(self):
        super().__init__(
            response_cls=ImportacaoResponse,
            raspagem_cls=ImportacaoRaspagem,
            repository=ImportacaoRepository(),
            logger=logger
        )


    def _transformar_json_para_modelo(self, dados_json: dict) -> Importacao:
        return Importacao(**dados_json)
