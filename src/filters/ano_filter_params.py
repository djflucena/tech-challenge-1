from pydantic import BaseModel
from pydantic import Field


class AnoVitiviniculturaFilterParams(BaseModel):
    """
    Parâmetro de filtro para os dados de vitivinicultura,
    incluindo Produção e Comercialização 
    de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    model_config = {"extra": "forbid"}
    
    ano: int = Field(
        ge=1970, le=2023,
        description="""Ano de referência para dados de vitivinicultura 
        (produção e comercialização) do Rio Grande do Sul."""
    )

