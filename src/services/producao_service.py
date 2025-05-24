import logging

from src.config.logging_config import configurar_logging
from src.raspagem.producao_raspagem import ProducaoRaspagem
from src.repositories.producao_repository import ProducaoRepository
from src.schemas import Producao, ProducaoResponse, Produto, Tipo
from src.services.base_service import BaseService


configurar_logging()
logger = logging.getLogger(__name__)


class ProducaoService(BaseService[ProducaoResponse]):

    def __init__(self):
        super().__init__(
            response_cls=ProducaoResponse,
            raspagem_cls=ProducaoRaspagem,
            repository=ProducaoRepository(),
            logger=logger
        )

       
    def _transformar_json_para_modelo(self, dados_json: dict) -> Producao:
        produtos = []

        for item in dados_json["Produto"]:
            # Extrai o nome e a quantidade do produto (chave única por item)

            nome_produto = next(k for k in item.keys() if k != "TIPOS")
            qtd_produto = item[nome_produto]

            tipos = []
            for tipo in item.get("TIPOS", []):
                nome_tipo = next(iter(tipo))
                qtd_tipo = tipo[nome_tipo]
                tipos.append(Tipo(nome=nome_tipo, quantidade=qtd_tipo))

            produtos.append(Produto(
                                nome=nome_produto,
                                quantidade=qtd_produto,
                                tipo=tipos))

        return Producao(produto=produtos, total=dados_json["Total"])
