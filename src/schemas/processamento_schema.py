from pydantic import BaseModel, ConfigDict
from typing import List

from src.schemas.base_schema import BaseResponse


class TipoItem(BaseModel):
    nome: str
    quantidade: int


class CategoriaItem(BaseModel):
    categoria: str
    quantidade: int
    tipos: List[TipoItem]


class Processamento(BaseModel):
    cultivar: List[CategoriaItem]
    total: int

    model_config = ConfigDict(from_attributes=True)


class ProcessamentoResponse(BaseResponse):
    data: Processamento
