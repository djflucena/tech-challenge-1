# src/repositories/raw_repository.py
"""Repositório genérico para qualquer endpoint de vitivinicultura."""

from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from src.database import SessionLocal
from src.repositories.raw import RawVitiviniculturaCurrent
from src.repositories.exceptions import (
    ErroConexaoBD,
    ErroConsultaBD,
    RegistroNaoEncontrado,
)

class RawRepository:
    def __init__(self, categoria: str, has_subopcao: bool = False):
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
        Lança:
            ValueError: se esta categoria exige subopcao e subopcao for None.
            ErroConexaoBD: em falha ao conectar ou transacionar com o banco.
            ErroConsultaBD: em falha ao executar a consulta/upsert no banco.
        """
        # pré‐validação de subopcao
        if not self._has_subopcao:
            pk_sub = ""
        else:
            if subopcao is None:
                raise ValueError(f"{self._endpoint!r} exige subopcao")
            pk_sub = subopcao

        # tentativa de escrita no banco
        try:
            now = datetime.now(timezone.utc)
            insert_stmt = insert(RawVitiviniculturaCurrent).values(
                endpoint=self._endpoint,
                ano=ano,
                subopcao=pk_sub,
                fetched_at=now,
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

        except OperationalError as e:
            raise ErroConexaoBD(str(e))
        except SQLAlchemyError as e:
            raise ErroConsultaBD(str(e))

    def get_por_ano(
        self,
        ano: int,
        subopcao: str | None = None,
    ) -> dict:
        """
        Busca o registro em raw_vitivinicultura para o ano (e subopcao).

        Parâmetros:
            ano (int): ano dos dados.
            subopcao (str | None): subcategoria, se aplicável.

        Retorna:
            dict com chaves "data" e "fetched_at".

        Lança:
            ValueError: se esta categoria exige subopcao e subopcao for None.
            ErroConexaoBD: em falha ao conectar ou transacionar com o banco.
            ErroConsultaBD: em falha ao executar a consulta no banco.
            RegistroNaoEncontrado: se não existir nenhum registro para os parâmetros.
        """
        if not self._has_subopcao:
            pk_sub = ""
        else:
            if subopcao is None:
                raise ValueError(f"{self._endpoint!r} exige subopcao")
            pk_sub = subopcao

        try:
            with SessionLocal() as session:
                stmt = select(RawVitiviniculturaCurrent).filter_by(
                    endpoint=self._endpoint,
                    ano=ano,
                    subopcao=pk_sub
                )
                row = session.execute(stmt).scalars().first()

        except OperationalError as e:
            raise ErroConexaoBD(str(e))

        except SQLAlchemyError as e:
            raise ErroConsultaBD(str(e))

        if not row:
            raise RegistroNaoEncontrado(self._endpoint, ano, pk_sub)

        return {
            "data":       row.payload,
            "fetched_at": row.fetched_at
        }