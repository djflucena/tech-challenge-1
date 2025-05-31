from datetime import datetime

from src.raspagem.processamento_raspagem import ProcessamentoRaspagem
from src.repositories.processamento_repository import ProcessamentoRepository
from src.schemas.processamento_schema import (CategoriaItem, Processamento,
                                              ProcessamentoResponse, TipoItem)
from src.services.base_service import BaseService


class ProcessamentoService(BaseService):
    """
    Service para Processamento de uvas do Rio Grande do Sul.
    """
    def __init__(self):
        super().__init__(repository=ProcessamentoRepository())

    
    def get_raspagem(self, ano: int, subopcao: str) -> ProcessamentoRaspagem:
        return ProcessamentoRaspagem(ano, subopcao)
    

    def get_reponse(self, source: str, fetched_at: datetime, data: dict) -> ProcessamentoResponse:
        return ProcessamentoResponse(
            source = source,
            fetched_at = fetched_at, 
            data = self._transformar_json_para_modelo(data)
        )


    def _transformar_json_para_modelo(self, dados_json: dict) -> Processamento:
        categorias = []

        table_header = 'Cultivar' if 'Cultivar' in dados_json else 'Sem definição'

        for item in dados_json[table_header]:
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
