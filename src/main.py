from typing import Annotated
from fastapi import Query
from fastapi import HTTPException

from src.config import app
from src.config import URL_BASE
from src.services.producao_services import ProducaoService
from src.filters.ano_filter_params import AnoFilterParams

@app.get(URL_BASE+"/producao")
async def producao(
    ano_filter: Annotated[
        AnoFilterParams, 
        Query(description="""Ano de produção dos vinhos, 
              sucos e derivados do Rio Grande do Sul.""")
        ]):
    """
        Endpoint para retornar a produção de vinhos, 
        sucos e derivados do Rio Grande do Sul.
    """
    try:
        return ProducaoService().get_por_ano(ano_filter.ano)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get(URL_BASE+"/importacao")
async def importacao(
    ano_filter: Annotated[
        AnoFilterParams, 
        Query(description="""Ano de produção dos vinhos e tipos de vinhos""")
        ]):
    """
        Endpoint para retornar dados de importação de derivados de uva.
    """
    try:
        return ProducaoService().get_por_ano(ano_filter.ano)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))