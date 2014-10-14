"""empty message

Revision ID: 3c13f01fa0fa
Revises: None
Create Date: 2014-10-14 14:38:09.926131

"""

# revision identifiers, used by Alembic.
revision = '3c13f01fa0fa'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=True),
    sa.Column('cellphone', sa.String(length=11), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_cellphone'), 'users', ['cellphone'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_cellphone'), table_name='users')
    op.drop_table('users')
    ### end Alembic commands ###
