from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from src.database import SessionLocal
from src.repositories.raw import RawVitiviniculturaCurrent
from sqlalchemy import select
class RawRepository:
    def upsert(
        self,
        endpoint: str,
        ano: int,
        subopcao: str | None,
        payload: dict
    ) -> None:
        """
        Insere ou atualiza (upsert) um registro na tabela raw_vitivinicultura.

        Se já existir um registro com a mesma chave primária (endpoint, ano, subopcao),
        os campos 'payload' e 'fetched_at' serão atualizados.

        Parâmetros:
            endpoint (str): Nome do endpoint (ex: 'comercializacao', 'producao').
            ano (int): Ano dos dados.
            subopcao (str | None): Subcategoria opcional. Usa string vazia se None.
            payload (dict): Dados a serem armazenados no formato JSON.
        """
        pk_sub = subopcao if subopcao is not None else ""
        insert_stmt = insert(RawVitiviniculturaCurrent).values(
            endpoint=endpoint,
            ano=ano,
            subopcao=pk_sub,
            fetched_at=datetime.now(timezone.utc),
            payload=payload
        )

        upsert_stmt = insert_stmt.on_conflict_do_update(
            index_elements=["endpoint", "ano", "subopcao"],
            set_={
                "payload":    insert_stmt.excluded.payload,
                "fetched_at": insert_stmt.excluded.fetched_at,
            }
        )

        with SessionLocal() as session:
            session.execute(upsert_stmt)
            session.commit()

    def get(
        self,
        endpoint: str,
        ano: int,
        subopcao: str | None
    ) -> dict | None:
        """
        Busca um registro da tabela raw_vitivinicultura com base nos filtros fornecidos.

        Parâmetros:
            endpoint (str): Nome do endpoint (ex: 'comercializacao', 'producao').
            ano (int): Ano dos dados.
            subopcao (str | None): Subcategoria opcional. Usa string vazia se None.

        Retorna:
            dict | None: O conteúdo armazenado em 'payload' se encontrado, caso contrário None.
        """
        try:
            pk_sub = subopcao or ""
            with SessionLocal() as session:
                stmt = select(RawVitiviniculturaCurrent).filter_by(
                    endpoint=endpoint,
                    ano=ano,
                    subopcao=pk_sub
                )
                row = session.execute(stmt).scalars().first()
                return row.payload if row else None
        except Exception as e:
            print(f"Erro ao buscar dados do banco: {e}")
            return None

