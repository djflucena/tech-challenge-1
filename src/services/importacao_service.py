import logging
from datetime import datetime

from src.config.logging_config import configurar_logging
from src.raspagem.importacao_raspagem import ImportacaoRaspagem
from src.repositories.importacao_repository import ImportacaoRepository
from src.schemas.importacao_schema import Importacao, ImportacaoResponse
from src.services.base_service import BaseService


configurar_logging()
logger = logging.getLogger(__name__)


class ImportacaoService(BaseService):
    """
    Service para importação de vinhos, sucos e derivados do Rio Grande do Sul.
    """

    def __init__(self):
        super().__init__(repository=ImportacaoRepository(), logger=logger)


    def get_raspagem(self, ano: int, subopcao: str) -> ImportacaoRaspagem:
        return ImportacaoRaspagem(ano, subopcao)


    def get_reponse(self, source: str, fetched_at: datetime, data: dict) -> ImportacaoResponse:
        return ImportacaoResponse(
            source = source, 
            fetched_at = fetched_at, 
            data = Importacao(**data)
        )
