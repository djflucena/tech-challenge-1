import logging

from src.config.logging_config import configurar_logging
from src.raspagem.exportacao_raspagem import ExportacaoRaspagem
from src.repositories.exportacao_repository import ExportacaoRepository
from src.schemas.exportacao_schema import Exportacao, ExportacaoResponse
from src.services.base_service import BaseService


configurar_logging()
logger = logging.getLogger(__name__)

class ExportacaoService(BaseService[ExportacaoResponse]):
    """
    Service para exportação de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    def __init__(self):
        super().__init__(
            response_cls=ExportacaoResponse,
            raspagem_cls=ExportacaoRaspagem,
            repository=ExportacaoRepository(),
            logger=logger
        )


    def _transformar_json_para_modelo(self, dados_json: dict) -> Exportacao:
        return Exportacao(**dados_json)
