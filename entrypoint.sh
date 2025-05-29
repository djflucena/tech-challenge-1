#!/usr/bin/env bash
set -e

echo "🔌 Aguardando o Postgres via DATABASE_URL..."
until psql "$DATABASE_URL" -c '\q'; do
  sleep 1
done

echo "✅ Postgres disponível!"

echo "📦 Aplicando migrações Alembic..."
alembic upgrade head

: "${PORT:=8000}"
exec uvicorn src.main:app --host 0.0.0.0 --port "$PORT"