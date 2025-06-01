"""Atualiza view processamento para usar coalesce em Cultivar

Revision ID: c526de0c4302
Revises: dc006cd04c26
Create Date: 2025-05-31 20:11:20.972142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c526de0c4302'
down_revision: Union[str, None] = 'dc006cd04c26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: recria a view 'processamento' usando coalesce em 'Cultivar'."""
    op.execute("""
    create or replace view vitivinicultura.processamento as
    select
        r.ano,
        r.subopcao,
        -- rótulo legível para cada sub-opção
        case
            r.subopcao
            when 'subopt_01' then 'Viníferas'
            when 'subopt_02' then 'Americanas e híbridas'
            when 'subopt_03' then 'Uvas de mesa'
            when 'subopt_04' then 'Sem classificação'
            else r.subopcao
        end as subopcao_desc,
        kv.control as control,
        -- nome do produto-pai
        kv.is_subitem,
        -- true se for subitem, false caso contrário
        kv.key as cultivar,
        -- nome do (sub)item
        (kv.value)::float as kilogramas
    from
        vitivinicultura.raw_vitivinicultura as r
        -- explode o array: primeiro tenta "Cultivar", se não existir, usa "Sem definicao"
    cross join lateral
        jsonb_array_elements(
            coalesce(
                r.payload->'Cultivar',
                r.payload->'Sem definicao',
                '[]'::jsonb
            )
        ) as prod(element)
        -- une itens principais e subitens, mantendo control e is_subitem
    cross join lateral (
        -- 1) itens de nível principal: é o próprio grupo ("TINTAS", "BRANCAS E ROSADAS", ...)
        select
            elem.key,
            elem.value,
            false as is_subitem,
            elem.key as control
        from
            jsonb_each(prod.element) as elem
        where
            elem.key <> 'TIPOS'
    union all
        -- 2) subitens dentro de "TIPOS": cada variedade de uva
        select
            sub.key,
            sub.value,
            true as is_subitem,
            parent.control
        from
            (
            -- produto-pai (o mesmo elem.key acima)
            select
                key as control
            from
                jsonb_each(prod.element)
            where
                key <> 'TIPOS'
            limit 1
        ) as parent
        cross join lateral
            jsonb_array_elements(prod.element->'TIPOS') as tipo(item)
        cross join lateral
            jsonb_each(tipo.item) as sub(key, value)
    ) as kv
    where
        r.endpoint = 'processamento'
    order by
        r.ano,
        kv.control,
        kv.is_subitem,
        kv.key;
    """)


def downgrade() -> None:
    """Downgrade schema: restaura a view 'processamento' para a versão anterior (sem coalesce)."""
    op.execute("""
    create or replace view vitivinicultura.processamento as
    select
        r.ano,
        r.subopcao,
        case
            r.subopcao
            when 'subopt_01' then 'Viníferas'
            when 'subopt_02' then 'Americanas e híbridas'
            when 'subopt_03' then 'Uvas de mesa'
            when 'subopt_04' then 'Sem classificação'
            else r.subopcao
        end as subopcao_desc,
        kv.control as control,
        kv.is_subitem,
        kv.key as cultivar,
        (kv.value)::float as kilogramas
    from
        vitivinicultura.raw_vitivinicultura as r
        -- explode o array "Cultivar"
    cross join lateral
        jsonb_array_elements(r.payload->'Cultivar') as prod(element)
        -- une itens principais e subitens, mantendo control e is_subitem
    cross join lateral (
        select
            elem.key,
            elem.value,
            false as is_subitem,
            elem.key as control
        from
            jsonb_each(prod.element) as elem
        where
            elem.key <> 'TIPOS'
    union all
        select
            sub.key,
            sub.value,
            true as is_subitem,
            parent.control
        from
            (
            select
                key as control
            from
                jsonb_each(prod.element)
            where
                key <> 'TIPOS'
            limit 1
        ) as parent
        cross join lateral
            jsonb_array_elements(prod.element->'TIPOS') as tipo(item)
        cross join lateral
            jsonb_each(tipo.item) as sub(key, value)
    ) as kv
    where
        r.endpoint = 'processamento'
    order by
        r.ano,
        kv.control,
        kv.is_subitem,
        kv.key;
    """)