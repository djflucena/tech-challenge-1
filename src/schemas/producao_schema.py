from pydantic import BaseModel, ConfigDict
from typing import List

from src.schemas.base_schema import BaseResponse


class TipoItem(BaseModel):
    nome: str
    quantidade: int


class ProdutoItem(BaseModel):
    nome: str
    quantidade: int
    tipo: List[TipoItem]


class Producao(BaseModel):
    produto: List[ProdutoItem]
    total: int

    model_config = ConfigDict(from_attributes=True)


class ProducaoResponse(BaseResponse):
    data: Producao
