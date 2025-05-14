from typing import Annotated
from fastapi import Query

from src.config import app
from src.services.producao_services import ProducaoService
from src.filters.ano_filter_params import AnoFilterParams

URL_BASE = "/vitivinicultura/api/v1"

@app.get(URL_BASE+"/producao")
async def producao(
    ano: Annotated[
        AnoFilterParams, 
        Query(description="""Ano de produção dos vinhos, 
              sucos e derivados do Rio Grande do Sul.""")
        ]):
    """
        Endpoint para retornar a produção de vinhos, 
        sucos e derivados do Rio Grande do Sul.
    """
    return ProducaoService().get_por_ano(ano)