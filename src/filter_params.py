from pydantic import BaseModel
from pydantic import Field

class AnoFilterParams(BaseModel):
    """
        Parâmetro de filtro para a produção de vinhos, 
        sucos e derivados do Rio Grande do Sul.
    """
    model_config = {"extra": "forbid"}
    ano: int = Field(
        ge=1970, le=2023, 
        description="""Ano de produção dos vinhos, 
        sucos e derivados do Rio Grande do Sul."""
        )
    