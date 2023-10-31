"""member board_id eliminate

Revision ID: d420b87a3ca7
Revises: b507969cd9d7
Create Date: 2023-07-25 19:57:09.076087

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd420b87a3ca7'
down_revision = 'b507969cd9d7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('member_ibfk_1', 'member', type_='foreignkey')
    op.drop_column('member', 'board_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('member', sa.Column('board_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('member_ibfk_1', 'member', 'board', ['board_id'], ['id_id'])
    # ### end Alembic commands ###
