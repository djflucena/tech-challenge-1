FROM python:3.10-slim

WORKDIR /app

# Instala o cliente psql (e limpa cache de apt)
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código + entrypoint
COPY . .
RUN chmod +x /app/entrypoint.sh

# Expõe a porta
EXPOSE 8000

# Define variáveis de ambiente padrão do DB (podem ser sobrescritas no compose)
ENV DB_HOST=db
ENV DB_PORT=5432

# Usa o entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
