"""empty message

Revision ID: 15ab7485ee21
Revises: 455c6932f220
Create Date: 2020-06-13 13:10:28.768695

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '15ab7485ee21'
down_revision = '455c6932f220'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sysaccess',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=20), nullable=False),
    sa.Column('senha', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('login'),
    sa.UniqueConstraint('senha')
    )
    op.drop_index('login', table_name='funcionario')
    op.drop_index('senha', table_name='funcionario')
    op.drop_column('funcionario', 'senha')
    op.drop_column('funcionario', 'login')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('funcionario', sa.Column('login', mysql.VARCHAR(length=20), nullable=False))
    op.add_column('funcionario', sa.Column('senha', mysql.VARCHAR(length=20), nullable=False))
    op.create_index('senha', 'funcionario', ['senha'], unique=True)
    op.create_index('login', 'funcionario', ['login'], unique=True)
    op.drop_table('sysaccess')
    # ### end Alembic commands ###
