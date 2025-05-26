import logging
from datetime import datetime

from src.config.logging_config import configurar_logging
from src.raspagem.comercializacao_raspagem import ComercializacaoRaspagem
from src.repositories.comercializacao_repository import ComercializacaoRepository
from src.schemas.comercializacao_schema import (Comercializacao, ComercializacaoResponse,
                                                ProdutoItem, TipoItem)
from src.services.base_service import BaseService


configurar_logging()
logger = logging.getLogger(__name__)


class ComercializacaoService(BaseService):

    def __init__(self):
        super().__init__(repository=ComercializacaoRepository(), logger=logger)


    def get_raspagem(self, ano: int, subopcao: str) -> ComercializacaoRaspagem:
        return ComercializacaoRaspagem(ano, subopcao)
    

    def get_reponse(self, source: str, fetched_at: datetime, data: dict) -> ComercializacaoResponse:
        return ComercializacaoResponse(
            source = source,
            fetched_at = fetched_at, 
            data = self._transformar_json_para_modelo(data)
        )


    def _transformar_json_para_modelo(self, dados_json: dict) -> Comercializacao:
        produtos = []
        
        for item in dados_json["Produto"]:
            nome_produto = next(k for k in item.keys() if k != "TIPOS")
            qtd_produto = item[nome_produto]

            tipos = []
            for tipo in item.get("TIPOS", []):
                nome_tipo = next(iter(tipo))
                qtd_tipo = tipo[nome_tipo]
                tipos.append(TipoItem(nome=nome_tipo, quantidade=qtd_tipo))

            produtos.append(ProdutoItem(nome=nome_produto, quantidade=qtd_produto, tipo=tipos))
            
        return Comercializacao(produto=produtos, total=dados_json["Total"])
