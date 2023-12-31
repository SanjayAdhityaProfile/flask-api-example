"""table creations

Revision ID: 9bc06e50bc90
Revises: 
Create Date: 2023-07-22 17:06:12.531966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bc06e50bc90'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('board_id', sa.VARCHAR(length=36), nullable=True),
    sa.Column('name', sa.VARCHAR(length=36), nullable=False),
    sa.Column('description', sa.VARCHAR(length=250), nullable=False),
    sa.Column('is_active', sa.Enum('active', 'un_activate', name='isactiveenum'), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id_id')
    )
    op.create_index(op.f('ix_board_created_at'), 'board', ['created_at'], unique=False)
    op.create_index(op.f('ix_board_id_id'), 'board', ['id_id'], unique=False)
    op.create_index(op.f('ix_board_is_active'), 'board', ['is_active'], unique=False)
    op.create_table('team',
    sa.Column('id_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('password_hash', sa.String(length=150), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('about', sa.String(length=140), nullable=True),
    sa.Column('admin_name', sa.String(length=20), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id_id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_team_email'), 'team', ['email'], unique=True)
    op.create_table('member',
    sa.Column('id_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=140), nullable=True),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=36), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id_id'], ),
    sa.PrimaryKeyConstraint('id_id')
    )
    op.create_table('ticket',
    sa.Column('id_id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('status', sa.Integer(), nullable=False),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id_id'], ),
    sa.PrimaryKeyConstraint('id_id')
    )
    op.create_index(op.f('ix_ticket_timestamp'), 'ticket', ['timestamp'], unique=False)
    op.create_table('member_board',
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('board_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['board_id'], ['board.id_id'], ),
    sa.ForeignKeyConstraint(['member_id'], ['member.id_id'], )
    )
    op.create_table('member_ticket',
    sa.Column('member_id', sa.Integer(), nullable=True),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['member_id'], ['member.id_id'], ),
    sa.ForeignKeyConstraint(['ticket_id'], ['ticket.id_id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('member_ticket')
    op.drop_table('member_board')
    op.drop_index(op.f('ix_ticket_timestamp'), table_name='ticket')
    op.drop_table('ticket')
    op.drop_table('member')
    op.drop_index(op.f('ix_team_email'), table_name='team')
    op.drop_table('team')
    op.drop_index(op.f('ix_board_is_active'), table_name='board')
    op.drop_index(op.f('ix_board_id_id'), table_name='board')
    op.drop_index(op.f('ix_board_created_at'), table_name='board')
    op.drop_table('board')
    # ### end Alembic commands ###
