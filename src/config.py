import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:exemplo@localhost:5433/vitivinicultura"
)

# agora pega a URL da Embrapa via env var
URL_SITE_EMBRAPA = os.getenv(
    "URL_SITE_EMBRAPA",
    "http://vitibrasil.cnpuv.embrapa.br/index.php"
)