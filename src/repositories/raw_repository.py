from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from src.database import SessionLocal
from src.repositories.raw import RawVitiviniculturaCurrent

class RawRepository:
    def upsert(
        self,
        endpoint: str,
        ano: int,
        subopcao: str | None,
        payload: dict
    ) -> None:
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