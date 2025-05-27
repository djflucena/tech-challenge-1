from fastapi import Query
from pydantic import BaseModel, Field
from typing import Literal


class AnoSubopcaoImportacaoFilterParams(BaseModel):
    """
    Parâmetros de filtro para o ano e subopção de importação.
    """
    model_config = {"extra": "forbid"}
    ano: int = Field(
        ge=1970, le=2024, 
        description="""Ano de importação dos vinhos, 
        sucos e derivados do Rio Grande do Sul."""
        )
    subopcao: Literal["subopt_01","subopt_02","subopt_03",
                      "subopt_04","subopt_05"] = Query(
                                                ..., description="""
    subopt_01: Vinho de mesa,
    subopt_02: Espumante,
    subopt_03: Uvas frescas,
    subopt_04: Uvas passas,
    subopt_05: Sucos de uva
    """
                        )
    
class AnoSubopcaoExportacaoFilterParams(BaseModel):
    """
    Parâmetros de filtro para o ano e subopção de importação.
    """
    model_config = {"extra": "forbid"}
    ano: int = Field(
        ge=1970, le=2024, 
        description="""Ano de importação dos vinhos, 
        sucos e derivados do Rio Grande do Sul."""
        )
    subopcao: Literal["subopt_01","subopt_02",
                      "subopt_03","subopt_04"] = Query(
                                                ..., description="""
    subopt_01: Vinhos de mesa,
    subopt_02: Espumantes,
    subopt_03: Uvas frescas,
    subopt_04: Sucos de uva
    """
                        )
    

class AnoSubopcaoProcessamentoFilterParams(BaseModel):
    """
    Parâmetros de filtro para o ano e subopção de processamento.
    """
    model_config = {"extra": "forbid"}

    ano: int = Field(
        ge=1970,
        le=2023,
        description="""Ano de referência para dados de processamento 
        de uvas viníferas, americanas, de mesa e sem classificação."""
    )

    subopcao: Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"] = Query(
        ...,
        description="""
        subopt_01: Viníferas,
        subopt_02: Americanas e híbridas,
        subopt_03: Uvas de mesa,
        subopt_04: Sem classificação
        """
                        )
