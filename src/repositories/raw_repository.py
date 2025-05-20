# src/repositories/raw_repository.py
"""Repositório genérico para qualquer endpoint de vitivinicultura."""

from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from src.database import SessionLocal
from src.repositories.raw import RawVitiviniculturaCurrent

class RawRepository:
    def __init__(self, categoria: str, has_subopcao: bool):
        """
        Repositório genérico para qualquer endpoint de vitivinicultura.
        Guarda internamente o nome do endpoint (categoria) e se aceita subopcao.
        """
        self._endpoint = categoria
        self._has_subopcao = has_subopcao

    def salvar_ou_atualizar(
        self,
        dados: dict,
        ano: int,
        subopcao: str | None = None,
    ) -> None:
        """
        Insere ou atualiza um registro na tabela raw_vitivinicultura.

        Parâmetros:
            dados (dict): payload a ser salvo.
            ano (int): ano dos dados.
            subopcao (str | None): subcategoria, se aplicável.
        """
        if not self._has_subopcao:
            pk_sub = ""
        else:
            if subopcao is None:
                raise ValueError(f"{self._endpoint!r} exige subopcao")
            pk_sub = subopcao

        insert_stmt = insert(RawVitiviniculturaCurrent).values(
            endpoint=self._endpoint,
            ano=ano,
            subopcao=pk_sub,
            fetched_at=datetime.now(timezone.utc),
            payload=dados
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

    def get_por_ano(
        self,
        ano: int,
        subopcao: str | None = None,
    ) -> dict | None:
        """
        Busca o registro em raw_vitivinicultura para o ano (e subopcao).

        Parâmetros:
            ano (int): ano dos dados.
            subopcao (str | None): subcategoria, se aplicável.

        Retorna:
            dict com chaves "data" e "fetched_at", ou None se não existir.
        """

        try:
            if not self._has_subopcao:
                pk_sub = ""
            else:
                if subopcao is None:
                    raise ValueError(f"{self._endpoint!r} exige subopcao")
                pk_sub = subopcao

            with SessionLocal() as session:
                stmt = select(RawVitiviniculturaCurrent).filter_by(
                    endpoint=self._endpoint,
                    ano=ano,
                    subopcao=pk_sub
                )
                row = session.execute(stmt).scalars().first()
                if not row:
                    return None

                return {
                    "data":        row.payload,
                    "fetched_at":  row.fetched_at
                }
        except Exception as e:
            print(f"Erro ao buscar dados do banco: {e}")
            return None