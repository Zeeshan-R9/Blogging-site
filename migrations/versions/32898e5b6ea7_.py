"""empty message

Revision ID: 32898e5b6ea7
Revises: c536190d7951
Create Date: 2024-01-27 00:45:19.644496

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32898e5b6ea7'
down_revision = 'c536190d7951'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=64), nullable=True))
        batch_op.add_column(sa.Column('passwd_hash', sa.String(length=128), nullable=True))
        batch_op.create_index(batch_op.f('ix_users_email'), ['email'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_users_email'))
        batch_op.drop_column('passwd_hash')
        batch_op.drop_column('email')

    # ### end Alembic commands ###