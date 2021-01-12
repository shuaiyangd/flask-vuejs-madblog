"""add notifications table

Revision ID: 03fc7ae17e63
Revises: 7f0adde79e8b
Create Date: 2021-01-12 14:41:12.676667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03fc7ae17e63'
down_revision = '7f0adde79e8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_notifications_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_notifications_timestamp'), ['timestamp'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_notifications_timestamp'))
        batch_op.drop_index(batch_op.f('ix_notifications_name'))

    op.drop_table('notifications')
    # ### end Alembic commands ###