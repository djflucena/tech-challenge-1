"""create raw_vitivinicultura_current

Revision ID: adae35424e47
Revises: 
Create Date: 2025-05-17 17:01:06.219165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adae35424e47'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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


def downgrade() -> None:
    # Drop índice e tabela principal
    op.drop_index('idx_raw_vitivinicultura_data_gin', table_name='raw_vitivinicultura', schema='vitivinicultura')
    op.drop_table('raw_vitivinicultura', schema='vitivinicultura')

    # Drop do schema, pois não é usado por mais nada
    op.execute("drop schema if exists vitivinicultura cascade")
