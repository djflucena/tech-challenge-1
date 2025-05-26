import logging
from datetime import datetime

from src.config.logging_config import configurar_logging
from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from src.repositories.exportacao_repository import ExportacaoRepository
from src.schemas.exportacao_schema import Exportacao, ExportacaoResponse
from src.services.base_service import BaseService


configurar_logging()
logger = logging.getLogger(__name__)


class ExportacaoService(BaseService):
    """
    Service para exportação de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    def __init__(self):
        super().__init__(repository=ExportacaoRepository(), logger=logger)


    def get_raspagem(self, ano: int, subopcao: str) -> ExportacaoRaspagem:
        return ExportacaoRaspagem(ano, subopcao)

    
    def get_reponse(self, source: str, fetched_at: datetime, data: dict) -> ExportacaoResponse:
        return ExportacaoResponse(
            source = source,
            fetched_at = fetched_at, 
            data = Exportacao(**data)
        )
