"""empty message

Revision ID: 1b9c3e4609b0
Revises: None
Create Date: 2014-10-19 22:54:34.539730

"""

# revision identifiers, used by Alembic.
revision = '1b9c3e4609b0'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('registers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('location', sa.Integer(), nullable=True),
    sa.Column('cellphone', sa.CHAR(length=11), nullable=True),
    sa.Column('name', sa.Unicode(length=8), nullable=True),
    sa.Column('need', sa.Unicode(length=64), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.Unicode(length=24), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('sex', sa.Boolean(), nullable=True),
    sa.Column('cellphone', sa.CHAR(length=11), nullable=True),
    sa.Column('address', sa.Unicode(length=128), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('remark', sa.Unicode(length=300), nullable=True),
    sa.Column('canceled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Unicode(length=256), nullable=True),
    sa.Column('age_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('intro', sa.UnicodeText(), nullable=True),
    sa.Column('closed', sa.Boolean(), nullable=True),
    sa.Column('page_view', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Unicode(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('site_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cellphone', sa.CHAR(length=11), nullable=True),
    sa.Column('body', sa.UnicodeText(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('age', sa.Unicode(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activity_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=True),
    sa.Column('body', sa.UnicodeText(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organizations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cellphone', sa.CHAR(length=11), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('member_since', sa.TIMESTAMP(), nullable=True),
    sa.Column('type', sa.Integer(), nullable=True),
    sa.Column('name', sa.Unicode(length=256), nullable=True),
    sa.Column('contact', sa.Unicode(length=16), nullable=True),
    sa.Column('address', sa.Unicode(length=512), nullable=True),
    sa.Column('authorization', sa.CHAR(length=32), nullable=True),
    sa.Column('photo', sa.CHAR(length=32), nullable=True),
    sa.Column('profession', sa.Integer(), nullable=True),
    sa.Column('property_', sa.Integer(), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('location', sa.Integer(), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('intro', sa.UnicodeText(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('page_view', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('email_confirmed', sa.Boolean(), nullable=True),
    sa.Column('cellphone', sa.String(length=11), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('member_since', sa.TIMESTAMP(), nullable=True),
    sa.Column('last_login', sa.TIMESTAMP(), nullable=True),
    sa.Column('identity', sa.CHAR(length=44), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_cellphone'), 'users', ['cellphone'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('classes_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=True),
    sa.Column('body', sa.UnicodeText(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.Unicode(length=256), nullable=True),
    sa.Column('age_id', sa.Integer(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('consult_time', sa.Unicode(length=128), nullable=True),
    sa.Column('start_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('end_time', sa.TIMESTAMP(), nullable=True),
    sa.Column('try_', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('intro', sa.UnicodeText(), nullable=True),
    sa.Column('closed', sa.Boolean(), nullable=True),
    sa.Column('page_view', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('organization_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('stars', sa.Integer(), nullable=True),
    sa.Column('body', sa.UnicodeText(), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('disabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('professions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('profession', sa.Unicode(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('activity_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('activity_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.TIMESTAMP(), nullable=True),
    sa.Column('name', sa.Unicode(length=24), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('sex', sa.Boolean(), nullable=True),
    sa.Column('cellphone', sa.CHAR(length=11), nullable=True),
    sa.Column('address', sa.Unicode(length=128), nullable=True),
    sa.Column('timestamp', sa.TIMESTAMP(), nullable=True),
    sa.Column('remark', sa.Unicode(length=300), nullable=True),
    sa.Column('canceled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('properties',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('property', sa.Unicode(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sizes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('size', sa.Unicode(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('times',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.Unicode(length=16), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.Unicode(length=6), nullable=True),
    sa.Column('district', sa.Unicode(length=9), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('class_time',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('class_id', sa.Integer(), nullable=True),
    sa.Column('time_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('class_time')
    op.drop_table('locations')
    op.drop_table('times')
    op.drop_table('sizes')
    op.drop_table('properties')
    op.drop_table('activity_orders')
    op.drop_table('professions')
    op.drop_table('organization_comments')
    op.drop_table('classes')
    op.drop_table('classes_comments')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_cellphone'), table_name='users')
    op.drop_table('users')
    op.drop_table('organizations')
    op.drop_table('activity_comments')
    op.drop_table('ages')
    op.drop_table('site_comments')
    op.drop_table('types')
    op.drop_table('activities')
    op.drop_table('class_orders')
    op.drop_table('registers')
    ### end Alembic commands ###
