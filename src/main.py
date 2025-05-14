from src.config import app
from src.services import ProducaoService

URL_BASE = "/vitivinicultura/api/v1"

@app.get(URL_BASE+"/producao")
async def producao(ano: int):
    return ProducaoService().get_por_ano(ano)