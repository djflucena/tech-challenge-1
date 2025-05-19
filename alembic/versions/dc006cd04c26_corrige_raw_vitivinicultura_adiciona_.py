"""Corrige raw_vitivinicultura: adiciona schema & views

Revision ID: dc006cd04c26
Revises: adae35424e47
Create Date: 2025-05-19 17:22:36.879697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc006cd04c26'
down_revision: Union[str, None] = 'adae35424e47'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Garante que o schema existe
    op.execute("create schema if not exists vitivinicultura;")

    # Cria tabela principal
    op.create_table(
        'raw_vitivinicultura',
        sa.Column('endpoint',    sa.Text,      nullable=False),
        sa.Column('ano',         sa.Integer,   nullable=False),
        sa.Column('subopcao',    sa.Text,      nullable=True),
        sa.Column('fetched_at',  sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('payload',     sa.JSON,      nullable=False),
        sa.PrimaryKeyConstraint('endpoint', 'ano', 'subopcao'),
        schema='vitivinicultura'
    )

    ## Converte payload de JSON para JSONB
    op.execute("""
    alter table vitivinicultura.raw_vitivinicultura
      alter column payload type jsonb
      using payload::jsonb;
    """)

    # Índice GIN sobre payload
    op.create_index(
        'idx_raw_vitivinicultura_data_gin',
        'raw_vitivinicultura',
        ['payload'],
        unique=False,
        postgresql_using='gin',
        schema='vitivinicultura'
    )

    # Tabela de histórico
    op.create_table(
        'raw_vitivinicultura_history',
        sa.Column('endpoint',    sa.Text,      nullable=False),
        sa.Column('ano',         sa.Integer,   nullable=False),
        sa.Column('subopcao',    sa.Text,      nullable=True),
        sa.Column('fetched_at',  sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('payload',     sa.JSON,      nullable=False),
        sa.Column('operation',   sa.CHAR(length=1), nullable=False),
        schema='vitivinicultura'
    )

    ## Converte payload de JSON para JSONB
    op.execute("""
    alter table vitivinicultura.raw_vitivinicultura_history
      alter column payload type jsonb
      using payload::jsonb;
    """)

    # Função de trigger para gravar histórico
    op.execute("""
    create or replace function vitivinicultura.fn_hist_raw()
    returns trigger as $$
    begin
    if tg_op = 'DELETE' then
        insert into vitivinicultura.raw_vitivinicultura_history
        select old.*, 'D';
    elsif tg_op = 'UPDATE' then
        begin
        insert into vitivinicultura.raw_vitivinicultura_history
        select new.*, 'U';
        exception when unique_violation then
        -- ignora ou atualiza?
        -- opcional: update vitivinicultura_history set ... where ...
        raise notice 'Histórico já existe para (% % %)', new.endpoint, new.ano, new.subopcao;
        end;
    elsif tg_op = 'INSERT' then
        insert into vitivinicultura.raw_vitivinicultura_history
        select new.*, 'I';
    end if;
    return null;
    end;
    $$ language plpgsql;
    """)

    # Trigger que dispara a função
    op.execute("""
    create or replace trigger trg_hist_raw
        after insert or update or delete
        on vitivinicultura.raw_vitivinicultura
        for each row execute function vitivinicultura.fn_hist_raw();
    """)

    # Views
    ## Produção
    op.execute("""
    create or replace view vitivinicultura.producao as
    select
        r.ano,
        kv.control as control,
        -- o nome do item-pai
        kv.is_subitem,
        -- true se for subitem, false caso contrário
        kv.key as produto,
    (kv.value)::float as litros
    from
        vitivinicultura.raw_vitivinicultura r
        -- 1) explode o array "Produto"
    cross join lateral
    jsonb_array_elements(r.payload->'Produto') as prod(element)
        -- 2) para cada elemento, faz um lateral join que
        --    retorna tanto o par principal (key/value) quanto os subitens
    cross join lateral (
        -- 2a) entrada de nível principal: is_subitem = false, control = própria chave
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
        -- 2b) subitens dentro de "TIPOS": is_subitem = true,
        --     control = nome do produto-pai
        select
            sub.key,
            sub.value,
            true as is_subitem,
            parent.control
        from
            (
            -- pega o nome do produto-pai (exatamente o mesmo elem.key acima)
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
        r.endpoint = 'producao'
    order by 
        r.ano,
        kv.control,
        -- agrupa por produto-pai
        kv.is_subitem,
        -- principal primeiro (false), depois subitens (true)
        kv.key;
    """)

    ## Comercialização
    op.execute("""
    create or replace view vitivinicultura.comercializacao as
    select
        r.ano,
        kv.control as control,
        -- o nome do item-pai
        kv.is_subitem,
        -- true se for subitem, false caso contrário
        kv.key as produto,
        (kv.value)::float as litros
    from
        vitivinicultura.raw_vitivinicultura r
        -- explode o array "Produto"
    cross join lateral
    jsonb_array_elements(r.payload->'Produto') as prod(element)
        -- junta itens principais e subitens, mantendo control e is_subitem
    cross join lateral (
        -- 1) itens de nível principal: is_subitem = false, control = própria chave
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
        -- 2) subitens dentro de "TIPOS": is_subitem = true, control = nome do produto-pai
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
        r.endpoint = 'comercializacao'
    order by
        r.ano,
        kv.control,
        kv.is_subitem,
        kv.key;
    """)

    ## Processamento
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
        -- explode o array "Cultivar"
    cross join lateral
    jsonb_array_elements(r.payload->'Cultivar') as prod(element)
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

    ## Importação
    op.execute("""
    create or replace view vitivinicultura.importacao as
    select
        r.ano,
        r.subopcao,
        case
            r.subopcao
        when 'subopt_01' then 'Vinho de mesa'
            when 'subopt_02' then 'Espumante'
            when 'subopt_03' then 'Uvas frescas'
            when 'subopt_04' then 'Uvas passas'
            when 'subopt_05' then 'Sucos de uva'
            else r.subopcao
        end as subopcao_desc,
        pais_item.item->>'pais' as pais,
        (pais_item.item->>'valor_us')::float as valor_us,
        (pais_item.item->>'quantidade_kg')::float as kilogramas
    from
        vitivinicultura.raw_vitivinicultura as r
    cross join lateral
    jsonb_array_elements(r.payload->'paises') as pais_item(item)
    where
        r.endpoint = 'importacao'
    order by ano, subopcao, pais;
    """)

    ## Exportação
    op.execute("""
    create or replace view vitivinicultura.exportacao as
    select
        r.ano,
        r.subopcao,
        case
            r.subopcao
        when 'subopt_01' then 'Vinhos de mesa'
            when 'subopt_02' then 'Espumantes'
            when 'subopt_03' then 'Uvas frescas'
            when 'subopt_04' then 'Sucos de uva'
            else r.subopcao
        end as subopcao_desc,
        pais_item.item->>'pais' as pais,
        (pais_item.item->>'valor_us')::float as valor_us,
        (pais_item.item->>'quantidade_kg')::float as kilogramas
    from
        vitivinicultura.raw_vitivinicultura as r
    cross join lateral
    jsonb_array_elements(r.payload->'paises') as pais_item(item)
    where
        r.endpoint = 'exportacao'
    order by
        ano,
        subopcao,
        pais;
    """)

def downgrade():
    # Remove views
    op.execute("drop view if exists vitivinicultura.exportacao")
    op.execute("drop view if exists vitivinicultura.importacao")
    op.execute("drop view if exists vitivinicultura.processamento")
    op.execute("drop view if exists vitivinicultura.comercializacao")
    op.execute("drop view if exists vitivinicultura.producao")
    
    # Remove trigger
    op.execute("drop trigger if exists trg_hist_raw on vitivinicultura.raw_vitivinicultura")

    # Remove função de trigger
    op.execute("drop function if exists vitivinicultura.fn_hist_raw() cascade")

    # Drop tabela de histórico
    op.drop_table('raw_vitivinicultura_history', schema='vitivinicultura')

    # Drop índice e tabela principal
    op.drop_index('idx_raw_vitivinicultura_data_gin', table_name='raw_vitivinicultura', schema='vitivinicultura')
    op.drop_table('raw_vitivinicultura', schema='vitivinicultura')

    # Drop do schema, pois não é usado por mais nada
    op.execute("drop schema if exists vitivinicultura cascade")
