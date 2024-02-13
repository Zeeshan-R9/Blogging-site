"""empty message

Revision ID: 76f9af635e48
Revises: 32898e5b6ea7
Create Date: 2024-01-27 01:37:52.690614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76f9af635e48'
down_revision = '32898e5b6ea7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('passwd_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('passwd_hash',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=128),
               existing_nullable=True)

    # ### end Alembic commands ###