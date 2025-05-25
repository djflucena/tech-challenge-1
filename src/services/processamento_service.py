import logging

from src.config.logging_config import configurar_logging
from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from src.repositories.processamento_repository import ProcessamentoRepository
from src.schemas.processamento_schema import (CategoriaItem, Processamento,
                                              ProcessamentoResponse, TipoItem)
from src.services.base_service import BaseService


configurar_logging()
logger = logging.getLogger(__name__)

class ProcessamentoService(BaseService[ProcessamentoResponse]):
    """
    Service para Processamento de uvas do Rio Grande do Sul.
    """

    def __init__(self):
        super().__init__(
            response_cls=ProcessamentoResponse,
            raspagem_cls=ProcessamentoRaspagem,
            repository=ProcessamentoRepository(),
            logger=logger
        )


    def _transformar_json_para_modelo(self, dados_json: dict) -> Processamento:
        categorias = []

        for item in dados_json["Cultivar"]:
            categoria = next(k for k in item if k != "TIPOS")
            quantidade = item[categoria]

            tipos = []
            for tipo in item["TIPOS"]:
                if not tipo:
                    continue
                nome, quantidade = next(iter(tipo.items()))
                tipos.append(TipoItem(nome=nome, quantidade=quantidade))

            categorias.append(CategoriaItem(
                categoria=categoria,
                quantidade=quantidade,
                tipos=tipos
            ))

        return Processamento(cultivar=categorias, total=dados_json["Total"])
