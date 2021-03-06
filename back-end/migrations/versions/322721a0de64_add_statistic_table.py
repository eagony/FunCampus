"""add statistic table

Revision ID: 322721a0de64
Revises: c5ca4f09d21f
Create Date: 2020-05-22 09:33:35.953441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '322721a0de64'
down_revision = 'c5ca4f09d21f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('statistics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=10), nullable=True),
    sa.Column('total_views', sa.Integer(), nullable=True),
    sa.Column('total_users', sa.Integer(), nullable=True),
    sa.Column('total_posts', sa.Integer(), nullable=True),
    sa.Column('total_comments', sa.Integer(), nullable=True),
    sa.Column('new_views', sa.Integer(), nullable=True),
    sa.Column('new_users', sa.Integer(), nullable=True),
    sa.Column('new_posts', sa.Integer(), nullable=True),
    sa.Column('new_comments', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_statistics'))
    )
    with op.batch_alter_table('statistics', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_statistics_date'), ['date'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('statistics', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_statistics_date'))

    op.drop_table('statistics')
    # ### end Alembic commands ###
