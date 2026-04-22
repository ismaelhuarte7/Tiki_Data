"""Add mvp_vote table

Revision ID: d2f7c1a1b3a0
Revises: b997ebcc018a
Create Date: 2026-04-20 12:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2f7c1a1b3a0'
down_revision = 'b997ebcc018a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'mvp_vote',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('match_id', sa.Integer(), nullable=False),
        sa.Column('voter_player_id', sa.Integer(), nullable=False),
        sa.Column('voted_player_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['match_id'], ['match.id']),
        sa.ForeignKeyConstraint(['voter_player_id'], ['player.id']),
        sa.ForeignKeyConstraint(['voted_player_id'], ['player.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('match_id', 'voter_player_id', name='uq_mvp_vote_match_voter')
    )
    op.create_index(op.f('ix_mvp_vote_match_id'), 'mvp_vote', ['match_id'], unique=False)
    op.create_index(op.f('ix_mvp_vote_voter_player_id'), 'mvp_vote', ['voter_player_id'], unique=False)
    op.create_index(op.f('ix_mvp_vote_voted_player_id'), 'mvp_vote', ['voted_player_id'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_mvp_vote_voted_player_id'), table_name='mvp_vote')
    op.drop_index(op.f('ix_mvp_vote_voter_player_id'), table_name='mvp_vote')
    op.drop_index(op.f('ix_mvp_vote_match_id'), table_name='mvp_vote')
    op.drop_table('mvp_vote')
