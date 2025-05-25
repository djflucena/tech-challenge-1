from pydantic import BaseModel, ConfigDict
from typing import List

from src.schemas.base_schema import BaseResponse


class PaisItem(BaseModel):
    pais: str
    quantidade_kg: int
    valor_us: int


class TotalItem(BaseModel):
    quantidade: int
    valor: int


class Importacao(BaseModel):
    paises: List[PaisItem]
    total: TotalItem

    model_config = ConfigDict(from_attributes=True)


class ImportacaoResponse(BaseResponse):
    data: Importacao