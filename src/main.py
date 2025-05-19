"""Controller para os endpoints da aplicação"""

from typing import Annotated
from fastapi import Query
from fastapi import HTTPException

from src.config import app
from src.config import URL_BASE
from src.services.importacao_service import ImportacaoService
from src.services.exportacao_service import ExportacaoService
from src.services.producao_services import ProducaoService
from src.services.comercializacao_services import ComercializacaoService
from src.services.processamento_service import ProcessamentoService
from src.filters.ano_filter_params import AnoVitiviniculturaFilterParams
from src.filters.ano_subopcao_param import AnoSubopcaoProcessamentoFilterParams
from src.filters.ano_subopcao_param import AnoSubopcaoImportacaoFilterParams
from src.filters.ano_subopcao_param import AnoSubopcaoExportacaoFilterParams
from src.config.logging_config import configurar_logging

configurar_logging()


@app.get(URL_BASE + "/producao")
async def producao(
    ano_filter: Annotated[
        AnoVitiviniculturaFilterParams,
        Query(
            description="""Ano de produção dos vinhos, 
              sucos e derivados do Rio Grande do Sul."""
        ),
    ],
):
    """
    Endpoint para retornar a produção de vinhos,
    sucos e derivados do Rio Grande do Sul.
    """
    try:
        return ProducaoService().get_por_ano(ano_filter.ano)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get(URL_BASE + "/comercializacao")
async def comercializacao(
    ano_filter: Annotated[
        AnoVitiviniculturaFilterParams,
        Query(
            description="""Ano de comercialização dos vinhos, 
              sucos e derivados do Rio Grande do Sul."""
        ),
    ],
):
    """
    Endpoint para retornar a comercialização de vinhos,
    sucos e derivados do Rio Grande do Sul.
    """
    try:
        return ComercializacaoService().get_por_ano(ano_filter.ano)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@app.get(URL_BASE + "/processamento")
async def processamento(
    params: Annotated[
        AnoSubopcaoProcessamentoFilterParams,
        Query(
            description="""Endpoint para retornar os dados de 
            processamento de uvas viníferas, americanas, de mesa 
            e sem classificação no Rio Grande do Sul."""
        ),
    ],
):
    """
    Endpoint para retornar os dados de processamento de uvas viníferas, 
    americanas, de mesa e sem classificação no Rio Grande do Sul.
    """
    try:
        return ProcessamentoService().get_por_ano(params.ano, params.subopcao)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@app.get(URL_BASE + "/importacao")
async def importacao(
    ano_subopcao_filter: Annotated[
        AnoSubopcaoImportacaoFilterParams,
        Query(description="""Ano de produção dos vinhos e tipos de vinhos"""),
    ],
):
    """
    Endpoint para retornar dados de importação de derivados de uva.
    """
    try:
        return ImportacaoService().get_por_ano(
            ano_subopcao_filter.ano, ano_subopcao_filter.subopcao
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e

@app.get(URL_BASE + "/exportacao")
async def exportacao(
    ano_subopcao_filter: Annotated[
        AnoSubopcaoExportacaoFilterParams,
        Query(description="""Ano de produção dos vinhos e tipos de vinhos"""),
    ],
):
    """
    Endpoint para retornar dados de exportação de derivados de uva.
    """
    try:
        return ExportacaoService().get_por_ano(
            ano_subopcao_filter.ano, ano_subopcao_filter.subopcao
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
