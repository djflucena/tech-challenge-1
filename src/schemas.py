from typing import List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class Tipo(BaseModel):
    nome: str
    quantidade: int


class Produto(BaseModel):
    nome: str
    quantidade: int
    tipo: List[Tipo]


class Producao(BaseModel):
    produto: List[Produto]
    total: int

    model_config = ConfigDict(from_attributes=True)


class BaseResponse(BaseModel):
    source: str
    fetched_at: datetime


class ProducaoResponse(BaseResponse):
    data: Producao

